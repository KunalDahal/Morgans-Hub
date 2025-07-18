from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from morgan_c.commands.admin import admin_only
from util import load_channels, save_channels, load_last_message_ids, save_last_message_ids

@admin_only
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /a <channel_id> <last_message_id>")
        return
    
    channel_id = context.args[0].strip()
    last_message_id = context.args[1].strip()
    
    try:
        channel_id_int = int(channel_id)
        last_message_id_int = int(last_message_id)
    except ValueError:
        await update.message.reply_text("❌ Both channel ID and last message ID must be numbers")
        return
    
    if channel_id_int > 0 or (channel_id_int < 0 and str(channel_id_int)[:4] != "-100"):
        await update.message.reply_text("❌ Invalid channel ID. Must be a supergroup/channel ID (starts with -100)")
        return
    
    channel_ids = load_channels()
    last_message_ids = load_last_message_ids()
    
    if channel_id_int in channel_ids:
        await update.message.reply_text("ℹ️ Channel already in monitoring list")
        return
    
    channel_ids.append(channel_id_int)
    last_message_ids[str(channel_id_int)] = last_message_id_int
    
    save_channels(channel_ids)
    save_last_message_ids(last_message_ids)
    await update.message.reply_text(f"✅ Channel added: {channel_id_int} with last message ID: {last_message_id_int}")

def get_add_channel_handler():
    return CommandHandler("a", add_channel)

@admin_only
async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /r <channel_id>")
        return
    
    try:
        channel_id = int(context.args[0].strip())
    except ValueError:
        await update.message.reply_text("❌ Invalid channel ID. Must be a number")
        return
    
    channel_ids = load_channels()
    last_message_ids = load_last_message_ids()
    
    if channel_id not in channel_ids:
        await update.message.reply_text("ℹ️ Channel not in monitoring list")
        return
    
    channel_ids.remove(channel_id)
    if str(channel_id) in last_message_ids:
        del last_message_ids[str(channel_id)]
    
    save_channels(channel_ids)
    save_last_message_ids(last_message_ids)
    await update.message.reply_text(f"✅ Channel removed: {channel_id}")

def get_remove_channel_handler():
    return CommandHandler("r", remove_channel)