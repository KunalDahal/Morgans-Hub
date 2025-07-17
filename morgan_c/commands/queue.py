from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from util import QUEUE_FILE
import json
import logging
from morgan_c.commands.admin import admin_only

logger = logging.getLogger(__name__)

@admin_only
async def queue_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /q command to show queue count"""
    try:
        with open(QUEUE_FILE, "r") as f:
            queue_data = json.load(f)
        
        count = len(queue_data)
        await update.message.reply_text(f"Current queue count: {count}")
        
    except Exception as e:
        logger.error(f"Error checking queue: {e}", exc_info=True)
        await update.message.reply_text("Error checking queue count.")

def get_queue_handler():
    return CommandHandler("q", queue_command)