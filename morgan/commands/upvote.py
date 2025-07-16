from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from util import save_upvotes, load_upvotes, format_text

async def upvote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /upvote command that shows count after first use"""
    user = update.effective_user
    if not user:
        if update.callback_query:
            await update.callback_query.answer("❌ Could not identify user.", show_alert=True)
        else:
            await update.message.reply_text(format_text("❌ Could not identify user."))
        return

    upvote_data = load_upvotes()
    
    if "users" not in upvote_data:
        upvote_data["users"] = {}
    
    if str(user.id) in upvote_data["users"]:
        if update.callback_query:
            await update.callback_query.answer(
                f"👍 Total Upvotes: {upvote_data.get('count', 0)}\n"
                "𝗦𝘁𝗮𝘆 𝘁𝘂𝗻𝗲𝗱, 𝗲𝘅𝗰𝗶𝘁𝗶𝗻𝗴 𝘁𝗶𝗺𝗲𝘀 𝗮𝗵𝗲𝗮𝗱!",
                show_alert=True
            )
        else:
            await update.message.reply_text(format_text(
                f"👍 Total Upvotes: {upvote_data.get('count', 0)}\n"
                "𝗦𝘁𝗮𝘆 𝘁𝘂𝗻𝗲𝗱, 𝗲𝘅𝗰𝗶𝘁𝗶𝗻𝗴 𝘁𝗶𝗺𝗲𝘀 𝗮𝗵𝗲𝗮𝗱!"
            ))
        return
    
    upvote_data["users"][str(user.id)] = True
    upvote_data["count"] = upvote_data.get("count", 0) + 1
    
    if save_upvotes(upvote_data):
        if update.callback_query:
            await update.callback_query.answer(
                "✅ Thank you for your upvote!\n"
                f"👍 Total Upvotes: {upvote_data['count']}\n"
                "𝗦𝘁𝗮𝘆 �𝘂𝗻𝗲𝗱, 𝗲𝘅𝗰𝗶𝘁𝗶𝗻𝗴 𝘁𝗶𝗺𝗲𝘀 𝗮𝗵𝗲𝗮𝗱!",
                show_alert=True
            )
        else:
            await update.message.reply_text(format_text(
                "✅ Thank you for your upvote!\n"
                f"👍 Total Upvotes: {upvote_data['count']}\n"
                "𝗦𝘁𝗮𝘆 𝘁𝘂𝗻𝗲𝗱, 𝗲𝘅𝗰𝗶𝘁𝗶𝗻𝗴 𝘁𝗶𝗺𝗲𝘀 𝗮𝗵𝗲𝗮𝗱!"
            ))
    else:
        if update.callback_query:
            await update.callback_query.answer("❌ Failed to save your upvote. Please try again.", show_alert=True)
        else:
            await update.message.reply_text(format_text("❌ Failed to save your upvote. Please try again."))

def get_upvote_handlers():
    """Return upvote command handler"""
    return [CommandHandler("upvote", upvote)]