import logging
import asyncio
from telegram import InputMediaPhoto, InputMediaVideo, Message
from util import get_target_channel

logger = logging.getLogger(__name__)

REQUEST_DELAY = 0.5  

async def get_media_group_messages(bot, message: Message):
    """Get all messages in a media group in correct order"""
    if not message.media_group_id:
        return [message]
    
    media_group = [message]
    try:
        updates = await bot.get_updates(offset=message.message_id - 20, timeout=5)
        
        for update in updates:
            if (update.message and 
                update.message.media_group_id == message.media_group_id and
                update.message.chat_id == message.chat_id and
                update.message.message_id != message.message_id):  
                media_group.append(update.message)
        
        media_group.sort(key=lambda m: m.message_id)
        
        unique_messages = []
        seen_ids = set()
        for msg in media_group:
            if msg.message_id not in seen_ids:
                seen_ids.add(msg.message_id)
                unique_messages.append(msg)
        
        return unique_messages
    
    except Exception as e:
        logger.error(f"Error getting media group: {e}")
        return [message]  

async def forward_media_group(bot, messages: list[Message], new_caption: str):
    """Forward media group only if it's a complete group"""
    targets = get_target_channel()
    if not targets or not messages:
        return
    
    if len(messages) == 1:
        logger.info(f"Skipping single message in media group (ID: {messages[0].media_group_id})")
        return
    
    media_group = []
    for i, message in enumerate(messages):
        if message.photo:
            media = InputMediaPhoto(
                media=message.photo[-1].file_id,
                caption=new_caption if i == 0 else None,
                parse_mode="MarkdownV2"
            )
        elif message.video:
            media = InputMediaVideo(
                media=message.video.file_id,
                caption=new_caption if i == 0 else None,
                parse_mode="MarkdownV2"
            )
        else:
            continue
        media_group.append(media)
    
    if not media_group:
        return
    
    for channel_id in targets:
        try:
            await bot.send_media_group(
                chat_id=channel_id,
                media=media_group
            )
            logger.info(f"Forwarded complete media group ({len(media_group)} items) to {channel_id}")
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Failed to forward to {channel_id}: {e}")

async def forward_to_targets(bot, message: Message, text: str):
    """Forward single message with simple rate limiting"""
    targets = get_target_channel()
    if not targets:
        await message.reply_text("No target channels configured!")
        return
    
    for channel_id in targets:
        try:
            if message.photo:
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=message.photo[-1].file_id,
                    caption=text,
                    parse_mode="MarkdownV2"
                )
            elif message.video:
                await bot.send_video(
                    chat_id=channel_id,
                    video=message.video.file_id,
                    caption=text,
                    parse_mode="MarkdownV2"
                )
            else:
                await bot.send_message(
                    chat_id=channel_id,
                    text=text,
                    parse_mode="MarkdownV2"
                )
            logger.info(f"Forwarded to channel {channel_id}")
            await asyncio.sleep(REQUEST_DELAY)
        except Exception as e:
            logger.error(f"Failed to forward to {channel_id}: {e}")