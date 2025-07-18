import logging
from telegram import Update, Message
from telegram.ext import ContextTypes, CommandHandler
from morgan.edit.editor import Editor
from morgan.admin import morgans_only
from util import format_text 

logger = logging.getLogger(__name__)

async def send_text_only_back(bot, text: str, chat_id: int):
    """Send edited text back to admin without any media"""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="MarkdownV2"
        )
        logger.info(f"Sent back edited text to admin {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send text back to admin: {e}")
        raise

@morgans_only
async def edit_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /edit command from admins to edit and get back the processed text"""
    user = update.effective_user
    if not user:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            format_text(
                """
❖ MORGANS HUB EDIT GUIDE ❖
✦─────────────────────────✦
Send your text ✉️
→ Keep it short or medium-short.
→ I'll edit it in MORGANS style: short, sharp, news-bold.
→ I may translate if needed (specify language: /edit it or /edit ru).
✦─────────────────────────✦
❖HOW TO EDIT❖

•Forward the message
•Reply with /edit it → Translate [Italian → English] + Formats
•Reply with /edit ru → Translate [Russian → English] + Formats
•Reply with /edit →  Formats

✦─────────────────────────✦
That's it. The news flies.
✦─────────────────────────✦
                """
            )
        )
        return

    original_message = update.message.reply_to_message
    editor = Editor()

    try:
        original_text = original_message.caption or original_message.text or ""
        
        translation_lang = None
        if context.args and len(context.args) > 0:
            lang_arg = context.args[0].lower()
            if lang_arg in ['it', 'ru']:
                translation_lang = lang_arg
        
        processed_text = await editor.process(original_text, translation_lang)

        status_msg = await update.message.reply_text(format_text("🔄 Processing your edit request..."))

        await send_text_only_back(context.bot, processed_text, update.effective_chat.id)

        await status_msg.edit_text(
            format_text(
                "✅ Successfully edited!"
            )
        )

    except Exception as e:
        logger.error(f"Admin edit error (User {user.id}): {e}")
        await update.message.reply_text(
            format_text(
                "❌ Failed to process edit request.\n"
                f"Error: {str(e)}"
            )
        )
        if 'status_msg' in locals():
            await status_msg.delete()

async def send_message_back(bot, message: Message, text: str, chat_id: int):
    """Send edited message back to admin"""
    try:
        if message.photo:
            await bot.send_photo(
                chat_id=chat_id,
                photo=message.photo[-1].file_id,
                caption=text,
                parse_mode="MarkdownV2"
            )
        elif message.video:
            await bot.send_video(
                chat_id=chat_id,
                video=message.video.file_id,
                caption=text,
                parse_mode="MarkdownV2"
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="MarkdownV2"
            )
        logger.info(f"Sent back edited message to admin {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send message back to admin: {e}")
        raise

def get_edit_admin_handler() -> CommandHandler:
    return CommandHandler("edit", edit_admin_command)