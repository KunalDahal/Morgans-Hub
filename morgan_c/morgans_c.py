import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)
from util import get_bot_token_2, get_admin_ids
from editor.editor import Editor
from morgan_c.forward import get_media_group_messages, forward_media_group, forward_to_targets
from importlib import reload
import editor.editor
from telegram import BotCommandScopeDefault, BotCommandScopeChat
from morgan_c.commands.banned import get_banned_handlers
from morgan_c.commands.channel import get_add_channel_handler, get_remove_channel_handler
from morgan_c.commands.help import get_help_handler
from morgan_c.commands.list import get_list_handlers
from morgan_c.commands.maintainence import get_maintenance_handlers
from morgan_c.commands.remove import get_add_remove_word_handler, get_remove_remove_word_handler
from morgan_c.commands.replace import get_rep_handlers
from morgan_c.commands.start import get_start_handler
from morgan_c.security import get_security_handlers

reload(editor.editor)
from editor.editor import Editor
editor = Editor()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Post initialization function to set bot commands based on user status"""
    public_commands = [
        ("start", "Start the bot"),
    ]
    
    admin_commands = public_commands + [
        ("help", "Show all available commands"),
        ("a", "Add source channel"),
        ("r", "Remove source channel"),
        ("ar", "Add word to removal list"),
        ("rr", "Remove word from removal list"),
        ("ab", "Add banned word"),
        ("rb", "Remove banned word"),
        ("arep", "Add replacement rule"),
        ("rrep", "Remove replacement rule"),
        ("lb", "List banned words"),
        ("lc", "List monitored channels"),
        ("lrm", "List remove words"),
        ("lrp", "List replace words"),
        ("lf", "List forward groups"),
        ("restart", "Restart the bot"),
        ("shutdown", "Shutdown the bot"),
        ("reset", "Reset JSON files"),
        ("reset_show", "Show resettable files"),
        ("health", "Check bot health"),
        ("ping", "Check bot latency")
    ]
    
    await application.bot.set_my_commands(
        public_commands,
        scope=BotCommandScopeDefault()
    )
    
    for admin_id in get_admin_ids():
        await application.bot.set_my_commands(
            admin_commands,
            scope=BotCommandScopeChat(admin_id)
        )


async def block_non_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Block text messages from non-admin users"""
    if update.message and update.message.text:
        await update.message.reply_text("Sorry, only admins can send text messages to this bot.")
        return
      
async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and forward admin messages with proper media group handling"""
    try:
        if update.message.media_group_id:
            if hasattr(context, 'processed_groups'):
                if update.message.media_group_id in context.processed_groups:
                    return
            else:
                context.processed_groups = set()
            
            messages = await get_media_group_messages(context.bot, update.message)
            
            context.processed_groups.add(update.message.media_group_id)
            
            if len(messages) > 1:
                caption = messages[0].caption if messages[0].caption else messages[0].text
                processed_text = await editor.process(caption) if caption else ""
                await forward_media_group(context.bot, messages, processed_text)
            return
        
        if not hasattr(update.message, 'media_group_id') or not update.message.media_group_id:
            content = update.message.caption if update.message.caption else update.message.text
            logger.info(f"Received message from {update.effective_user.id}:")
            logger.info(f"Content: '{content}'")
            logger.info(f"Message ID: {update.message.message_id}")
            logger.info(f"Media group ID: {getattr(update.message, 'media_group_id', 'N/A')}")
            
            processed_text = await editor.process(content) if content else ""
            logger.info(f"Processed text: '{processed_text}'")
            await forward_to_targets(context.bot, update.message, processed_text)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    """Start the bot with optimized connection settings"""
    application = Application.builder() \
        .token(get_bot_token_2()) \
        .connection_pool_size(8) \
        .pool_timeout(30) \
        .get_updates_pool_timeout(30) \
        .post_init(post_init) \
        .build()
    
    # Add security handlers
    for handler in get_security_handlers(): 
        application.add_handler(handler)    
    
    application.add_handler(get_start_handler())
    application.add_handler(get_help_handler())
    application.add_handler(get_add_channel_handler())
    application.add_handler(get_remove_channel_handler())
    
    for handler in get_banned_handlers():
        application.add_handler(handler)
    
    for handler in get_list_handlers():
        application.add_handler(handler)
    
    for handler in get_maintenance_handlers():
        application.add_handler(handler)
    
    for handler in get_rep_handlers():
        application.add_handler(handler)
    
    application.add_handler(get_add_remove_word_handler())
    application.add_handler(get_remove_remove_word_handler())
    
    admin_filter = filters.User(user_id=get_admin_ids())
    application.add_handler(MessageHandler(
        filters.TEXT & (~admin_filter), 
        block_non_admin_text
    ))
    application.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO & admin_filter,
        handle_admin_message
    ))

    application.run_polling()

if __name__ == '__main__':
    main()