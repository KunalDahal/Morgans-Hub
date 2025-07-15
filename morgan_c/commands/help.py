from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from morgan_c.commands.admin import admin_only

@admin_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command showing all available commands"""
    user = update.effective_user
    message = (
        "📋 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n\n"
        "🔍 𝗦𝗼𝘂𝗿𝗰𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗼𝗻𝗶𝘁𝗼𝗿𝗶𝗻𝗴:\n"
        "/a <ch\_id> - 𝗔𝗱𝗱/𝘂𝗽𝗱𝗮𝘁𝗲 𝘀𝗼𝘂𝗿𝗰𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹\n"
        "/r <ch\_id> - 𝗥𝗲𝗺𝗼𝘃𝗲 𝘀𝗼𝘂𝗿𝗰𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹\n\n"
        "🚫 𝗖𝗼𝗻𝘁𝗲𝗻𝘁 𝗙𝗶𝗹𝘁𝗲𝗿𝗶𝗻𝗴:\n"
        "/ar <word> - 𝗔𝗱𝗱 𝘁𝗼 𝗿𝗲𝗺𝗼𝘃𝗮𝗹 𝗹𝗶𝘀𝘁\n"
        "/rr <word> - 𝗥𝗲𝗺𝗼𝘃𝗲 𝗳𝗿𝗼𝗺 𝗿𝗲𝗺𝗼𝘃𝗮𝗹 𝗹𝗶𝘀𝘁\n"
        "/ab <word> - 𝗔𝗱𝗱 𝘁𝗼 𝗯𝗮𝗻𝗻𝗲𝗱 𝘄𝗼𝗿𝗱𝘀\n"
        "/rb <word> - 𝗥𝗲𝗺𝗼𝘃𝗲 𝗳𝗿𝗼𝗺 𝗯𝗮𝗻𝗻𝗲𝗱 𝘄𝗼𝗿𝗱𝘀\n\n"
        "🔄 𝗧𝗲𝘅𝘁 𝗥𝗲𝗽𝗹𝗮𝗰𝗲𝗺𝗲𝗻𝘁:\n"
        "/arep <old> <new> - 𝗔𝗱𝗱 𝗿𝗲𝗽𝗹𝗮𝗰𝗲𝗺𝗲𝗻𝘁 𝗿𝘂𝗹𝗲\n"
        "/rrep <old> - 𝗥𝗲𝗺𝗼𝘃𝗲 𝗿𝗲𝗽𝗹𝗮𝗰𝗲𝗺𝗲𝗻𝘁 𝗿𝘂𝗹𝗲\n\n"
        "📜 𝗟𝗶𝘀𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
        "/lb - 𝗟𝗶𝘀𝘁 𝗯𝗮𝗻𝗻𝗲𝗱 𝘄𝗼𝗿𝗱𝘀\n"
        "/lc - 𝗟𝗶𝘀𝘁 𝗺𝗼𝗻𝗶𝘁𝗼𝗿𝗲𝗱 𝘀𝗼𝘂𝗿𝗰𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀\n"
        "/lrm - 𝗟𝗶𝘀𝘁 𝗿𝗲𝗺𝗼𝘃𝗲 𝘄𝗼𝗿𝗱𝘀\n"
        "/lrp - 𝗟𝗶𝘀𝘁 𝗿𝗲𝗽𝗹𝗮𝗰𝗲 𝘄𝗼𝗿𝗱𝘀\n"
        "⚙️ 𝗦𝘆𝘀𝘁𝗲𝗺 𝗠𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲:\n"
        "/restart - 𝗥𝗲𝘀𝘁𝗮𝗿𝘁 𝘁𝗵𝗲 𝗯𝗼𝘁\n"
        "/shutdown - 𝗦𝗵𝘂𝘁𝗱𝗼𝘄𝗻 𝘁𝗵𝗲 𝗯𝗼𝘁\n"
        "/reset - 𝗥𝗲𝘀𝗲𝘁 𝗮𝗹𝗹 𝗝𝗦𝗢𝗡 𝗳𝗶𝗹𝗲𝘀\n"
        "/reset <file> - 𝗥𝗲𝘀𝗲𝘁 𝗮 �𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰 𝗝𝗦𝗢𝗡 𝗳𝗶𝗹𝗲\n"
        "/reset_show - 𝗦𝗵𝗼𝘄 𝗮𝗹𝗹 𝗿𝗲𝘀𝗲𝘁𝘁𝗮𝗯𝗹𝗲 𝗝𝗦𝗢𝗡 𝗳𝗶𝗹𝗲𝘀\n"
        "/health - 𝗕𝗼𝘁 𝗵𝗲𝗮𝗹𝘁𝗵 𝘀𝘁𝗮𝘁𝘂𝘀\n"
        "/ping - 𝗖𝗵𝗲𝗰𝗸 𝗯𝗼𝘁 𝗹𝗮𝘁𝗲𝗻𝗰𝘆\n\n"
        "👍 𝗨𝗽𝘃𝗼𝘁𝗲 𝗦𝘆𝘀𝘁𝗲𝗺:\n"
        "/upvote - 𝗦𝗵𝗼𝘄 𝘆𝗼𝘂𝗿 �𝘂𝗽𝗽𝗼𝗿𝘁 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗯𝗼𝘁 (𝗼𝗻𝗲 𝘁𝗶𝗺𝗲 𝗼𝗻𝗹𝘆)\n"
        "❓ 𝗛𝗲𝗹𝗽:\n"
        "/help - 𝗦𝗵𝗼𝘄 𝘁𝗵𝗶𝘀 𝗵𝗲𝗹𝗽 𝗺𝗲𝘀𝘀𝗮𝗴𝗲\n\n"
        f"🆔 𝗬𝗼𝘂𝗿 𝗨𝘀𝗲𝗿 𝗜𝗗: `{user.id}`"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

def get_help_handler():
    return CommandHandler("help", help_command)