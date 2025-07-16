from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from util import get_bot_username, format_text
import os
import logging

logger = logging.getLogger(__name__)

DRAMATIC_GIF_URL = os.path.join('IMAGE', 'stop.gif')

GIF_CAPTION = """

✦─────────────────────────✦
─ 𝗛𝗢𝗟𝗗 𝗜𝗧 𝗥𝗜𝗚𝗛𝗧 𝗧𝗛𝗘𝗥𝗘! ─
✦─────────────────────────✦

𝗧𝗵𝗶𝘀 𝗺𝗶𝗴𝗵𝘁𝘆 𝗯𝗶𝗿𝗱 𝗶𝘀𝗻’𝘁 𝘀𝗼𝗺𝗲 𝗰𝗼𝗺𝗺𝗼𝗻 𝗳𝗹𝗼𝗰𝗸 𝘀𝗾𝘂𝗮𝘄𝗸𝗲𝗿 —  
𝗜’𝗺 𝗮 𝗣𝗘𝗥𝗦𝗢𝗡𝗔𝗟 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗯𝗼𝘁, 𝗵𝗲𝗿𝗲 𝘁𝗼 𝘀𝗽𝗿𝗲𝗮𝗱 𝗵𝗲𝗮𝗱𝗹𝗶𝗻𝗲𝘀 𝘁𝗮𝗶𝗹𝗼𝗿𝗲𝗱 𝗷𝘂𝘀𝘁 𝗳𝗼𝗿 𝗬𝗢𝗨!

✦─────────────────────────✦

𝗖𝗿𝗮𝘃𝗶𝗻𝗴 𝘀𝗰𝗮𝗻𝗱𝗮𝗹𝗼𝘂𝘀 𝘁𝗮𝗹𝗲𝘀? 𝗪𝗼𝗿𝗹𝗱-𝘀𝗵𝗮𝗸𝗶𝗻𝗴 𝗻𝗲𝘄𝘀? 𝗥𝘂𝗺𝗼𝗿𝘀 𝘁𝗵𝗮𝘁 𝗿𝗮𝘁𝘁𝗹𝗲 𝘁𝗵𝗲 𝗚𝗿𝗮𝗻𝗱 𝗟𝗶𝗻𝗲?  
𝗧𝗵𝗲𝗻 𝗵𝗲𝗲𝗱 𝘁𝗵𝗶𝘀:

⇒ 𝗔𝗱𝗱 𝗺𝘆 𝗼𝘁𝗵𝗲𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝗻𝘀𝘁𝗲𝗮𝗱:  
@MorgansNews_Bot

✦─────────────────────────✦

𝗟𝗲𝘁 𝘁𝗵𝗶𝘀 𝗯𝗲 𝗰𝗮𝗿𝗿𝗶𝗲𝗱 𝗼𝗻 𝘁𝗵𝗲 𝘄𝗶𝗻𝗱𝘀 𝘁𝗼 𝗲𝘃𝗲𝗿𝘆 𝗰𝗼𝗿𝗻𝗲𝗿 𝗼𝗳 𝘁𝗵𝗲 𝘀𝗲𝗮𝘀!  
— 𝗠𝗼𝗿𝗴𝗮𝗻𝘀, 𝘀𝗼𝗮𝗿𝗶𝗻𝗴 𝗲𝘃𝗲𝗿 𝗵𝗶𝗴𝗵𝗲𝗿!

"""

async def handle_bot_added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when the bot is added to a group by leaving and sending a dramatic GIF."""
    try:
        # Check if the bot was added to a group
        if update.message and update.message.new_chat_members:
            bot_username = get_bot_username().lower()
            for member in update.message.new_chat_members:
                if member.username and member.username.lower() == bot_username:
                    # Get the user who added the bot
                    added_by = update.message.from_user
                    
                    # Send dramatic GIF with caption
                    await context.bot.send_animation(
                        chat_id=update.effective_chat.id,
                        animation=DRAMATIC_GIF_URL,
                        caption=GIF_CAPTION,
                        reply_to_message_id=update.message.message_id
                    )
                    
                    # Leave the group dramatically
                    await context.bot.leave_chat(update.effective_chat.id)
                    logger.info(f"Left group {update.effective_chat.id} after being added by {added_by.id}")
                    return
    except Exception as e:
        logger.error(f"Error handling group addition: {e}", exc_info=True)

def get_security_handlers():
    """Return security-related handlers"""
    return [
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_bot_added_to_group)
    ]