from monitor.hash.check import ContentChecker
import asyncio
import logging
import os
import time
import json
from collections import deque, defaultdict
from monitor.session import create_session
from util import get_bot_username, load_channels, get_dump_channel, QUEUE_FILE
from telethon.errors import ChannelPrivateError, ChannelInvalidError, FloodWaitError
from monitor.recovery import RecoverySystem
from monitor.forward import Forwarder
from telethon.tl.types import MessageService

logger = logging.getLogger(__name__)

class GlobalQueue:
    def __init__(self, filename):
        self.filename = filename
        self.queue = deque()
        self.load()
        
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.queue = deque(json.load(f))
            except Exception as e:
                logger.error(f"Error loading queue: {e}")
                self.queue = deque()
                
    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(list(self.queue), f)
        except Exception as e:
            logger.error(f"Error saving queue: {e}")
            
    async def add(self, item):
        """Add item to queue"""
        self.queue.append(item)
        self.save()
        
    async def get_next(self):
        """Get next item from queue"""
        if self.queue:
            item = self.queue.popleft()
            self.save()
            return item
        return None

class ChannelMonitor:
    def __init__(self):
        self.running = False
        self.client = create_session()
        self.bot_username = get_bot_username()
        self.channel_ids = set(load_channels())
        self.access_errors = defaultdict(int)
        self.content_checker = ContentChecker()
        self.recovery = RecoverySystem()
        self.queue = GlobalQueue(QUEUE_FILE)
        self.processing_semaphore = asyncio.Semaphore(3)
        self.message_batch_size = 10
        self.last_processed_time = defaultdict(float)

    async def run(self):
        self.running = True
        try:
            await self.client.connect()
            if not await self.client.is_user_authorized():
                logger.error("Session not authorized! Please run setup_session.py first.")
                await self.client.disconnect()
                return

            await self.client.start()
            logger.info("Telethon session started")
            logger.info("Starting monitoring with %d channels", len(self.channel_ids))
            
            tasks = [
                asyncio.create_task(self.queue_processor()),
                asyncio.create_task(self.continuous_monitor()),
                asyncio.create_task(self.channel_syncer())
            ]
            
            await asyncio.gather(*tasks)
                
        except Exception as e:
            logger.error(f"Monitor crashed: {e}", exc_info=True)
        finally:
            self.running = False
            await self.client.disconnect()

    async def continuous_monitor(self):
        """Continuous channel monitoring"""
        while self.running:
            try:
                await self.check_channels()
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(10)

    async def channel_syncer(self):
        """Sync channel states periodically"""
        while self.running:
            try:
                current_channels = set(load_channels())
                recovery_channels = set(self.recovery.last_message_ids.keys())
                
                for channel in current_channels - recovery_channels:
                    await self.recovery.initialize_channel_state(self.client, channel)
                    
                for channel in recovery_channels - current_channels:
                    self.recovery.remove_channel(channel)
                    
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Channel sync error: {e}")
                await asyncio.sleep(30)

    async def check_channels(self):
        """Check all channels for new messages"""
        for channel_id in list(self.channel_ids):
            if not self.running:
                break
                
            if self.access_errors.get(channel_id, 0) > 5:
                continue
                
            try:
                last_id = self.recovery.get_last_message_id(channel_id)
                await self._fetch_new_messages(channel_id, last_id)
                self.access_errors[channel_id] = 0
            except (ChannelPrivateError, ChannelInvalidError) as e:
                logger.error(f"No access to channel {channel_id}: {e}")
                self.access_errors[channel_id] += 1
            except FloodWaitError as e:
                logger.warning(f"Flood wait for {channel_id}: {e.seconds}s")
                await asyncio.sleep(e.seconds + 5)
            except Exception as e:
                logger.error(f"Error checking {channel_id}: {e}")
                self.access_errors[channel_id] += 1

    async def _fetch_new_messages(self, channel_id: int, last_id: int):
        """Fetch new messages and add to queue"""
        try:
            entity = await self.client.get_entity(channel_id)
            
            messages = await self.client.get_messages(
                entity,
                limit=1,
                min_id=last_id,
                reverse=True
            )

            if not messages:
                return
                
            newest_id = messages[0].id
            
            if newest_id > last_id:
                messages = await self.client.get_messages(
                    entity,
                    limit=self.message_batch_size,
                    min_id=last_id,
                    reverse=False
                )

                if messages:
                    valid_messages = [msg for msg in messages if not isinstance(msg, MessageService)]
                    if valid_messages:
                        await self._add_messages_to_queue(channel_id, valid_messages[::-1])
                        newest_id = valid_messages[-1].id
                        self.recovery.update_channel_state(channel_id, newest_id)
                
        except Exception as e:
            logger.error(f"Error fetching new messages for {channel_id}: {e}")
            raise

    async def _add_messages_to_queue(self, channel_id: int, messages: list):
        """Add messages to queue"""
        groups = defaultdict(list)
        
        for msg in messages:
            if msg.id <= self.recovery.get_last_message_id(channel_id):
                continue
                
            group_id = getattr(msg, "grouped_id", None)
            if group_id:
                groups[group_id].append(msg)
            else:
                await self.queue.add({
                    "channel_id": channel_id,
                    "message_ids": [msg.id],
                    "timestamp": time.time()
                })
        
        for group_messages in groups.values():
            await self.queue.add({
                "channel_id": channel_id,
                "message_ids": [msg.id for msg in group_messages],
                "timestamp": time.time()
            })

    async def queue_processor(self):
        """Process queue items"""
        logger.info("Queue processor started")
        while self.running:
            async with self.processing_semaphore:
                queue_item = await self.queue.get_next()
                if not queue_item:
                    await asyncio.sleep(1)
                    continue
                    
                try:
                    await self.process_queue_item(queue_item)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error processing queue item: {e}")
                    await asyncio.sleep(5)
                    await self.queue.add(queue_item)

    async def process_queue_item(self, item):
        """Process a single item from the queue"""
        channel_id = item["channel_id"]
        message_ids = item["message_ids"]
        
        try:
            entity = await self.client.get_entity(channel_id)
            messages = []
            for msg_id in message_ids:
                msg = await self.client.get_messages(entity, ids=msg_id)
                if msg and not isinstance(msg, MessageService):
                    messages.append(msg)
                    
            if not messages:
                return
                
            if len(messages) == 1:
                await self.process_single_message(messages[0])
            else:
                await self.process_media_group(messages)
                
        except Exception as e:
            logger.error(f"Error processing item from {channel_id}: {e}")
            
    async def process_single_message(self, message):
        """Process a single message"""
        channel_id = message.chat_id
        check_result = await self.content_checker.check_content(message)
        message_text = getattr(message, "message", "")
        
        if check_result == 1:
            logger.info(f"Skipping duplicate message {message.id} in {channel_id}")
            return
        
        forwarder = Forwarder(self.client)
        await forwarder.forward_with_retry(
            message, [message], message_text, channel_id, 0
        )

    async def process_media_group(self, messages):
        """Process a media group"""
        if not messages:
            return
            
        channel_id = messages[0].chat_id
        group_result = await self.content_checker.check_group_content(messages)
        
        clean_messages = group_result['clean_messages']
        if not clean_messages:
            logger.info(f"Skipping duplicate group in {channel_id}")
            return
            
        caption = group_result['original_caption']
        
        forwarder = Forwarder(self.client)
        await forwarder.forward_with_retry(
            messages, clean_messages, caption, channel_id, 0
        )