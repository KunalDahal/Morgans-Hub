# forward.py
import logging
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.errors import FloodWaitError
import asyncio
import random
from typing import List, Union
import os

logger = logging.getLogger(__name__)

class Forwarder:
    def __init__(self, client, bot_username):
        self.client = client
        self.bot_username = bot_username
        self.current_operations = {}  # Track ongoing operations per channel
        self.operation_lock = asyncio.Lock()  # Lock for operation tracking

    async def upload_and_send(self, message, caption: str, channel_id: int):
        """Forward or send media with Telegram-like compression"""
        try:
            logger.info(f"Channel {channel_id}: Processing message {message.id}")
            
            if message.media:
                # Try native forwarding first for better compression
                try:
                    return await self.client.forward_messages(
                        self.bot_username,
                        message,
                        from_peer=channel_id
                    )
                except Exception as forward_error:
                    logger.info(f"Channel {channel_id}: Native forward failed, falling back to upload: {forward_error}")
                    return await self._upload_media(message, caption, channel_id)
            else:
                logger.info(f"Channel {channel_id}: Sending text message to bot")
                return await self.client.send_message(
                    self.bot_username,
                    message.text if not caption else caption
                )
                
        except Exception as e:
            logger.error(f"Channel {channel_id}: Error uploading media: {e}")
            raise

    async def _upload_media(self, message, caption: str, channel_id: int):
        """Fallback media upload method"""
        try:
            if isinstance(message.media, MessageMediaPhoto):
                logger.info(f"Channel {channel_id}: Uploading photo to bot")
                return await self.client.send_file(
                    self.bot_username,
                    message.media,
                    caption=caption,
                    compress=True  # Enable compression
                )
            elif isinstance(message.media, MessageMediaDocument):
                if hasattr(message, 'document') and message.document.mime_type.startswith('video/'):
                    logger.info(f"Channel {channel_id}: Uploading video to bot")
                    return await self.client.send_file(
                        self.bot_username,
                        message.media,
                        caption=caption,
                        supports_streaming=True,
                        video_note=(message.document.mime_type == 'video/mp4')
                    )
                else:
                    logger.info(f"Channel {channel_id}: Uploading document to bot")
                    return await self.client.send_file(
                        self.bot_username,
                        message.media,
                        caption=caption
                    )
        except Exception as e:
            logger.error(f"Channel {channel_id}: Error in fallback media upload: {e}")
            raise

    async def send_media_group(self, messages: List, caption: str, channel_id: int):
        """Send media group using Telethon's native methods"""
        try:
            # Prepare media list for Telethon
            media_objects = []
            
            for i, msg in enumerate(messages):
                if not msg.media:
                    continue
                    
                logger.info(f"Channel {channel_id}: Processing media {i+1}/{len(messages)}")
                media_objects.append(msg.media)
            
            if media_objects:
                logger.info(f"Channel {channel_id}: Sending media group with {len(media_objects)} items")
                return await self.client.send_file(
                    self.bot_username,
                    media_objects,
                    caption=caption
                )
                
        except Exception as e:
            logger.error(f"Channel {channel_id}: Error sending media group: {e}")
            raise

    async def process_message(self, message: Union[List, object], clean_messages: List, original_caption: str, channel_id: int):
        """Process and send messages with detailed logging"""
        async with self.operation_lock:
            if channel_id in self.current_operations:
                logger.info(f"Channel {channel_id}: Waiting for existing operation to complete")
                await self.current_operations[channel_id]
            
            self.current_operations[channel_id] = asyncio.Event()
            
        try:
            logger.info(f"Channel {channel_id}: Starting upload for {len(clean_messages)} messages")
            
            # Handle single message
            if len(clean_messages) == 1:
                msg = clean_messages[0]
                return await self.upload_and_send(msg, original_caption, channel_id)
            
            # Handle media groups
            if len(clean_messages) > 1:
                return await self.send_media_group(clean_messages, original_caption, channel_id)
            
            return None
        finally:
            async with self.operation_lock:
                self.current_operations[channel_id].set()
                del self.current_operations[channel_id]
                logger.info(f"Channel {channel_id}: Completed upload operation")

    async def forward_with_retry(self, messages, clean_messages, original_caption, channel_id, max_retries=3):
        """Send messages with retry logic"""
        if not isinstance(clean_messages, list):
            clean_messages = [clean_messages]

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Channel {channel_id}: Forward attempt {attempt}/{max_retries}")
                
                result = await self.process_message(messages, clean_messages, original_caption, channel_id)
                
                if result:
                    logger.info(f"Channel {channel_id}: Forward successful on attempt {attempt}")
                    return result
                
            except FloodWaitError as e:
                wait_time = e.seconds + random.uniform(1, 5)
                logger.warning(f"Channel {channel_id}: Flood wait - Retry {attempt}/{max_retries} in {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Channel {channel_id}: Forward error on attempt {attempt}: {e}")
                wait_time = min(2 ** attempt, 60) * random.uniform(0.8, 1.2)
                await asyncio.sleep(wait_time)
        
        logger.error(f"Channel {channel_id}: Failed to forward after {max_retries} attempts")
        return None