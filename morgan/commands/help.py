# morgan/commands/help.py
import os
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from util import format_text

HELP_CAPTION = """
✦──────────────✦
I be Morgan, the news hawk!

✦ Forward the post here (hide caption & sender).
✦ Tap it, edit by translating to English & shorten it. Click OK.
✦ Run /edit — I’ll style it up.
✦ Copy my caption, edit the same post, replace text.
✦ Then forward it to the main channel.

✦ That’s how we fly sharp news across the seas!
✦──────────────✦
"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dispatch the imperial missive"""
    image_path = os.path.join('IMAGE', 'help.jpg')
    help=format_text(HELP_CAPTION)
    if os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=help,
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text(
            HELP_CAPTION + "\n\n[Official Seal Missing]",
            parse_mode='Markdown'
        )

def get_help_handler() -> CommandHandler:
    """Issue the imperial command handler"""
    return CommandHandler("help", help_command)