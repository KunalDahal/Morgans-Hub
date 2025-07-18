import logging
import asyncio
from telegram import InputMediaPhoto, InputMediaVideo, Message
from util import get_target_channel, get_dump_channel, CAPTION_LIMIT, BAN_FILE
import json

logger = logging.getLogger(__name__)

REQUEST_DELAY = 0.5  

def load_banned_words():
    try:
        with open(BAN_FILE, 'r') as f:
            data = json.load(f)
         
            if isinstance(data, list):
                return data
            return data.get('banned_words', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

BANNED_WORDS = load_banned_words()

def contains_banned_words(text):
    if not text or not BANNED_WORDS:
        return False
    
    text_lower = text.lower()
    
    for banned in BANNED_WORDS:
        if ' ' in banned: 
            if banned.lower() in text_lower:
                return True
        else:  
            words_in_text = text_lower.split()
            if banned.lower() in words_in_text:
                return True
    
    return False

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
    
    dump_channel = get_dump_channel()
    should_dump = new_caption and (contains_banned_words(new_caption) or len(new_caption.split()) > CAPTION_LIMIT)
    
    if should_dump:
        if not dump_channel:
            return
            
        try:
            media_group = []
            for message in messages:
                if message.photo:
                    media = InputMediaPhoto(
                        media=message.photo[-1].file_id,
                        caption=new_caption,
                        parse_mode="MarkdownV2"
                    )
                elif message.video:
                    media = InputMediaVideo(
                        media=message.video.file_id,
                        caption=new_caption,
                        parse_mode="MarkdownV2"
                    )
                else:
                    continue
                media_group.append(media)
            
            if media_group:
                await bot.send_media_group(
                    chat_id=dump_channel,
                    media=media_group
                )
                logger.info(f"Forwarded banned/long caption media group ({len(media_group)} items) to dump channel {dump_channel}")
                return
        except Exception as e:
            logger.error(f"Failed to forward to dump channel {dump_channel}: {e}")
    else:
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
    
    dump_channel = get_dump_channel()
    should_dump = text and (contains_banned_words(text) or len(text.split()) > CAPTION_LIMIT)
    
    if should_dump:
        if not dump_channel:
            return
            
        try:
            if message.photo:
                await bot.send_photo(
                    chat_id=dump_channel,
                    photo=message.photo[-1].file_id,
                    caption=text,
                    parse_mode="MarkdownV2"
                )
            elif message.video:
                await bot.send_video(
                    chat_id=dump_channel,
                    video=message.video.file_id,
                    caption=text,
                    parse_mode="MarkdownV2"
                )
            else:
                await bot.send_message(
                    chat_id=dump_channel,
                    text=text,
                    parse_mode="MarkdownV2"
                )
            logger.info(f"Forwarded banned/long caption message to dump channel {dump_channel}")
            return
        except Exception as e:
            logger.error(f"Failed to forward to dump channel {dump_channel}: {e}")
    else:
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