import logging
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, InputSingleMedia
from telethon.errors import FloodWaitError
import asyncio
import random
from typing import List, Union
from util import get_bot_username

logger = logging.getLogger(__name__)


class Forwarder:
    def __init__(self, client):
        self.client = client
        self.bot_username = get_bot_username()
        self.current_operations = {}
        self.operation_lock = asyncio.Lock()
        self.forward_delay = 1.0 

    async def upload_and_send(self, message, caption: str, channel_id: int, check_result: int):
        """Forward or send media with Telegram-like compression"""
        try:
            logger.info(f"Channel {channel_id}: Processing message {message.id}")

            await asyncio.sleep(self.forward_delay)
        
            if check_result == 1:
                logger.info(f"Skipping duplicate message {message.id}")
                return None
            if check_result == 0:  
                target = self.bot_username
            elif check_result == 3: 
                target = self.bot_username
            else: 
                pass

            if message.media:
                try:
                    return await self.client.forward_messages(
                        target, message, from_peer=channel_id
                    )
                except Exception as forward_error:
                    logger.info(
                        f"Channel {channel_id}: Native forward failed, falling back to upload: {forward_error}"
                    )
                    return await self._upload_media(message, caption, channel_id, target)
            else:
                logger.info(f"Channel {channel_id}: Sending text message to {target}")
                return await self.client.send_message(
                    target, message.text if not caption else caption
                )

        except Exception as e:
            logger.error(f"Channel {channel_id}: Error uploading media: {e}")
            raise

    async def _upload_media(self, message, caption: str, channel_id: int, target: str):
        """Fallback media upload method"""
        try:
            await asyncio.sleep(self.forward_delay)

            if isinstance(message.media, MessageMediaPhoto):
                logger.info(f"Channel {channel_id}: Uploading photo to {target}")
                return await self.client.send_file(
                    target,
                    message.media,
                    caption=caption,
                    compress=True,  
                )
            elif isinstance(message.media, MessageMediaDocument):
                if hasattr(
                    message, "document"
                ) and message.document.mime_type.startswith("video/"):
                    logger.info(f"Channel {channel_id}: Uploading video to {target}")
                    return await self.client.send_file(
                        target,
                        message.media,
                        caption=caption,
                        supports_streaming=True,
                        video_note=(message.document.mime_type == "video/mp4"),
                    )
                else:
                    logger.info(f"Channel {channel_id}: Uploading document to {target}")
                    return await self.client.send_file(
                        target, message.media, caption=caption
                    )
        except Exception as e:
            logger.error(f"Channel {channel_id}: Error in fallback media upload: {e}")
            raise

    async def send_media_group(self, messages: List, caption: str, channel_id: int, check_result: int):
        """Send media group with preserved caption"""
        try:
            await asyncio.sleep(self.forward_delay)
            
            
            target = self.bot_username if check_result == 0 else self.bot_username
            
            media_list = []
            for i, msg in enumerate(messages):
                if not msg.media:
                    continue
                    
                media = msg.media
                if hasattr(media, 'document'):
                    media = media.document
                elif hasattr(media, 'photo'):
                    media = media.photo
                   
                msg_caption = getattr(msg, "message", "") or (caption if i == 0 else "")
                
                media_list.append({
                    'media': media,
                    'caption': msg_caption,
                    'entities': getattr(msg, 'entities', None)
                })

            if not media_list:
                return None

            logger.info(f"Channel {channel_id}: Sending media group with {len(media_list)} items to {target}")
            
            return await self.client.send_file(
                target,
                [m['media'] for m in media_list],
                captions=[m['caption'] for m in media_list],
                caption=caption,  
                supports_streaming=True
            )

        except Exception as e:
            logger.error(f"Channel {channel_id}: Error sending media group: {e}")
            raise

    async def process_message(
        self,
        message: Union[List, object],
        clean_messages: List,
        original_caption: str,
        channel_id: int,
        check_result: int,
    ):

        if channel_id in self.current_operations:
            logger.info(
                f"Channel {channel_id}: Waiting for existing operation to complete"
            )
            await self.current_operations[channel_id]

        self.current_operations[channel_id] = asyncio.Event()

        try:
            logger.info(
                f"Channel {channel_id}: Starting upload for {len(clean_messages)} messages"
            )

            if len(clean_messages) == 1:
                msg = clean_messages[0]
                return await self.upload_and_send(msg, original_caption, channel_id, check_result)

            if len(clean_messages) > 1:
                return await self.send_media_group(
                    clean_messages, original_caption, channel_id, check_result
                )

            return None
        finally:
            self.current_operations[channel_id].set()
            del self.current_operations[channel_id]
            logger.info(f"Channel {channel_id}: Completed upload operation")

    async def forward_with_retry(
        self, messages, clean_messages, original_caption, channel_id, check_result, max_retries=3
    ):
        """Send messages with retry logic"""
        if not isinstance(clean_messages, list):
            clean_messages = [clean_messages]

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    f"Channel {channel_id}: Forward attempt {attempt}/{max_retries}"
                )

                result = await self.process_message(
                    messages, clean_messages, original_caption, channel_id, check_result
                )

                if result:
                    logger.info(
                        f"Channel {channel_id}: Forward successful on attempt {attempt}"
                    )
                    return result

            except FloodWaitError as e:
                wait_time = e.seconds + random.uniform(1, 5)
                logger.warning(
                    f"Channel {channel_id}: Flood wait - Retry {attempt}/{max_retries} in {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(
                    f"Channel {channel_id}: Forward error on attempt {attempt}: {e}"
                )
                wait_time = min(2**attempt, 60) * random.uniform(0.8, 1.2)
                await asyncio.sleep(wait_time)

        logger.error(
            f"Channel {channel_id}: Failed to forward after {max_retries} attempts"
        )
        return None