from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from util import load_users, save_users, load_upvotes, save_upvotes, format_text
import os

news="@Animes_News_Ocean"
author=f"@suu_111"
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with image, caption, and buttons"""
    user = update.effective_user
    users = load_users()
    
    if str(user.id) not in users:
        users.append(str(user.id))
        save_users(users)
    about = f"""
❖ 𝗠𝗼𝗿𝗴𝗮𝗻𝘀 𝗼𝗳 𝗢𝗻𝗲 𝗣𝗶𝗲𝗰𝗲 𝗮𝘁 𝘆𝗼𝘂𝗿 𝘀𝗲𝗿𝘃𝗶𝗰𝗲!

𝗜 𝗮𝗺 𝘁𝗵𝗲 𝗽𝗿𝗼𝘂𝗱 𝗻𝗲𝘄𝘀 𝗯𝗶𝗿𝗱 𝘀𝗼𝗮𝗿𝗶𝗻𝗴 𝗮𝗯𝗼𝘃𝗲 𝘁𝗵𝗲 𝗚𝗿𝗮𝗻𝗱 𝗟𝗶𝗻𝗲,
𝗱𝗲𝗹𝗶𝘃𝗲𝗿𝗶𝗻𝗴 𝘀𝘁𝗼𝗿𝗶𝗲𝘀 𝗳𝗿𝗼𝗺 𝗲𝘃𝗲𝗿𝘆 𝗰𝗼𝗿𝗻𝗲𝗿 𝗼𝗳 𝘁𝗵𝗶𝘀 𝘃𝗮𝘀𝘁 𝘄𝗼𝗿𝗹𝗱.
𝗔 𝗷𝗼𝘂𝗿𝗻𝗮𝗹𝗶𝘀𝘁 𝗯𝘆 𝗯𝗹𝗼𝗼𝗱 𝗮𝗻𝗱 𝗮 𝗿𝘂𝗺𝗼𝗿 𝗵𝗮𝘄𝗸 𝗯𝘆 𝘁𝗿𝗮𝗱𝗲 —
𝗜 𝗱𝗲𝗰𝗶𝗱𝗲 𝘄𝗵𝗮𝘁 𝗯𝗲𝗰𝗼𝗺𝗲𝘀 𝗵𝗲𝗮𝗱𝗹𝗶𝗻𝗲 𝗮𝗻𝗱 𝘄𝗵𝗮𝘁 𝗳𝗮𝗱𝗲𝘀 𝗶𝗻𝘁𝗼 𝘄𝗵𝗶𝘀𝗽𝗲𝗿𝘀.

✦─────────────────────────✦
❖ 𝗪𝗵𝗮𝘁 𝗱𝗼 𝗜 𝗯𝗿𝗶𝗻𝗴 𝘆𝗼𝘂? ❖
✦─────────────────────────✦
• 𝗔𝗻𝗶𝗺𝗲 𝗻𝗲𝘄𝘀 & 𝗱𝗼𝗻𝗴𝗵𝘂𝗮 𝘂𝗽𝗱𝗮𝘁𝗲𝘀
• 𝗠𝗮𝗻𝗴𝗮 & 𝗺𝗮𝗻𝗵𝘄𝗮 𝗿𝗲𝗹𝗲𝗮𝘀𝗲𝘀
• 𝗟𝗶𝗴𝗵𝘁 𝗻𝗼𝘃𝗲𝗹 𝘀𝗰𝗼𝗼𝗽𝘀
• 𝗞𝗼𝗿𝗲𝗮𝗻 𝗲𝗻𝘁𝗲𝗿𝘁𝗮𝗶𝗻𝗺𝗲𝗻𝘁 𝗯𝘂𝘇𝘇
• 𝗔𝗹𝗼𝗻𝗴 𝘄𝗶𝘁𝗵 𝘀𝗼𝗺𝗲 𝗟𝗶𝘃𝗲 𝗔𝗰𝘁𝗶𝗼𝗻 𝗖𝗿𝗮𝘇𝗲
• 𝗔𝗻𝗱 𝗮𝗹𝗹 𝘁𝗵𝗲 𝘀𝗽𝗶𝗰𝘆 𝗿𝘂𝗺𝗼𝗿𝘀 𝘁𝗵𝗮𝘁 𝗰𝗮𝗻 𝘁𝘂𝗿𝗻 𝘁𝗵𝗲 𝘄𝗼𝗿𝗹𝗱 𝘂𝗽𝘀𝗶𝗱𝗲 𝗱𝗼𝘄𝗻

✦─────────────────────────✦
𝗦𝘁𝗶𝗰𝗸 𝘄𝗶𝘁𝗵 𝗺𝗲, 𝗮𝗻𝗱 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽𝘀 𝘄𝗶𝗹𝗹 𝗻𝗲𝘃𝗲𝗿 𝗺𝗶𝘀𝘀 𝗮 𝗯𝗲𝗮𝘁
𝗼𝗳 𝘁𝗵𝗶𝘀 𝗲𝘃𝗲𝗿-𝘁𝘂𝗿𝗯𝘂𝗹𝗲𝗻𝘁 𝘄𝗼𝗿𝗹𝗱.
"""



    caption=format_text(about)

    image_path = os.path.join('IMAGE', 'start.jpg')
    
    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(open(image_path, 'rb'), caption=caption),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("About Me", callback_data="about_morgan")]
            ])
        )
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(image_path, 'rb'),
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("About Me", callback_data="about_morgan")]
            ])
        )

async def about_morgan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the About Me button press"""
    query = update.callback_query
    await query.answer()
    
    about_story = f"""
✦─────────────────────────✦
❖ 𝗔 𝗯𝗿𝗶𝗲𝗳 𝘁𝗮𝗹𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 𝘄𝗶𝗻𝗴𝘀... ❖
✦─────────────────────────✦
𝗢𝗻𝗰𝗲, 𝗜 𝘄𝗮𝘀 𝗻𝗼𝘁𝗵𝗶𝗻𝗴 — 𝗮 𝗺𝗲𝗿𝗲 𝗳𝗲𝗮𝘁𝗵𝗲𝗿 𝗹𝗼𝘀𝘁 𝗼𝗻 𝘁𝗵𝗲 𝘄𝗶𝗻𝗱,
𝗱𝗿𝗶𝗳𝘁𝗶𝗻𝗴 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝘁𝗵𝗲 𝘃𝗼𝗶𝗱 𝗼𝗳 𝗼𝗯𝘀𝗰𝘂𝗿𝗶𝘁𝘆.

𝗕𝘂𝘁 𝗱𝗮𝘆 𝗯𝘆 𝗱𝗮𝘆, 𝘀𝘁𝗼𝗿𝘆 𝗯𝘆 𝘀𝘁𝗼𝗿𝘆, 𝗜 𝗴𝗮𝘁𝗵𝗲𝗿𝗲𝗱 𝗿𝘂𝗺𝗼𝗿𝘀,
𝘀𝘁𝗶𝘁𝗰𝗵𝗲𝗱 𝘁𝗵𝗲𝗺 𝗶𝗻𝘁𝗼 𝗽𝗹𝘂𝗺𝗮𝗴𝗲, 𝗮𝗻𝗱 𝗿𝗼𝘀𝗲 𝗮𝗯𝗼𝘃𝗲 𝘁𝗵𝗲 𝗰𝗹𝗼𝘂𝗱𝘀.

𝗡𝗼𝘄, 𝘄𝗶𝘁𝗵 𝗺𝗶𝗴𝗵𝘁𝘆 𝘄𝗶𝗻𝗴𝘀 𝘀𝗽𝗿𝗲𝗮𝗱 𝘄𝗶𝗱𝗲 𝗮𝗰𝗿𝗼𝘀𝘀 𝘁𝗵𝗲 𝘀𝗸𝗶𝗲𝘀,
𝗜 𝘄𝗮𝘁𝗰𝗵 𝗼𝘃𝗲𝗿 𝘁𝗵𝗶𝘀 𝘄𝗿𝗲𝘁𝗰𝗵𝗲𝗱 𝘄𝗼𝗿𝗹𝗱, 𝗲𝗮𝗴𝗲𝗿 𝘁𝗼 𝗿𝗲𝘃𝗲𝗮𝗹 𝗶𝘁𝘀 𝗵𝗶𝗱𝗱𝗲𝗻 𝘁𝘂𝗿𝗻𝘀.

𝗜 𝗿𝗲𝘀𝗶𝗱𝗲 𝗶𝗻 ❖{news}❖,
𝗮𝗻𝗱 𝗶𝗳 𝗲𝘃𝗲𝗿 𝘆𝗼𝘂 𝗻𝗲𝗲𝗱 𝗮 𝗵𝗮𝗻𝗱, 𝗺𝘆 𝘀𝘁𝗲𝗮𝗱𝗳𝗮𝘀𝘁 𝗮𝗹𝗹𝘆 ❖{author}❖
𝘄𝗶𝗹𝗹 𝗯𝗲 𝘁𝗵𝗲𝗿𝗲 𝘁𝗼 𝗵𝗲𝗹𝗽.

✦─────────────────────────✦
𝗡𝗲𝘄𝘀 𝘀𝗵𝗮𝗽𝗲𝘀 𝘁𝗵𝗲 𝘄𝗼𝗿𝗹𝗱,
𝗮𝗻𝗱 𝗜'𝗺 𝘁𝗵𝗲 𝗼𝗻𝗲 𝗳𝗹𝗮𝗽𝗽𝗶𝗻𝗴 𝘁𝗵𝗲𝘀𝗲 𝘄𝗶𝗻𝗴𝘀 𝘁𝗼 𝗺𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝗶𝘁 𝗱𝗼𝗲𝘀.
"""
    
    about_image_path = os.path.join('IMAGE', 'about.jpg')
    
    await query.edit_message_media(
        media=InputMediaPhoto(open(about_image_path, 'rb'), caption=about_story),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Upvote Morgan", callback_data="upvote_morgan")],
            [InlineKeyboardButton("Back to Main", callback_data="main_menu")]
        ])
    )

async def show_upvote_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the upvote page with image and current count"""
    query = update.callback_query
    await query.answer()
    
    upvote_data = load_upvotes()
    count = upvote_data.get('count', 0)
    caption = f"""
❖ 𝗧𝗼𝘁𝗮𝗹 𝗨𝗽𝘃𝗼𝘁𝗲𝘀: {count} ❖
✦─────────────────────────✦
𝗬𝗼𝘂𝗿 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗵𝗲𝗹𝗽𝘀 𝗠𝗼𝗿𝗴𝗮𝗻𝘀 𝘀𝗼𝗮𝗿 𝗵𝗶𝗴𝗵𝗲𝗿,
𝘀𝗽𝗿𝗲𝗮𝗱𝗶𝗻𝗴 𝘁𝗵𝗲𝘀𝗲 𝗴𝗿𝗮𝗻𝗱 𝘄𝗶𝗻𝗴𝘀 𝗮𝗰𝗿𝗼𝘀𝘀 𝘁𝗵𝗲 𝘀𝗲𝗮𝘀.

𝗘𝘃𝗲𝗿𝘆 𝘂𝗽𝘃𝗼𝘁𝗲 𝗯𝗿𝗶𝗻𝗴𝘀 𝘂𝘀 𝗰𝗹𝗼𝘀𝗲𝗿 𝘁𝗼 𝗱𝗲𝗹𝗶𝘃𝗲𝗿𝗶𝗻𝗴 𝘁𝗵𝗲 𝗹𝗮𝘁𝗲𝘀𝘁:
• 𝗔𝗻𝗶𝗺𝗲 𝗵𝗲𝗮𝗱𝗹𝗶𝗻𝗲𝘀 & 𝗱𝗼𝗻𝗴𝗵𝘂𝗮 𝘂𝗽𝗱𝗮𝘁𝗲𝘀
• 𝗠𝗮𝗻𝗴𝗮 & 𝗺𝗮𝗻𝗵𝘄𝗮 𝗵𝗼𝘁 𝗱𝗿𝗼𝗽𝘀, 𝗔𝗹𝗼𝗻𝗴 𝘄𝗶𝘁𝗵 𝘀𝗼𝗺𝗲 𝗟𝗶𝘃𝗲 𝗔𝗰𝘁𝗶𝗼𝗻 𝗖𝗿𝗮𝘇𝗲
• 𝗟𝗶𝗴𝗵𝘁 𝗻𝗼𝘃𝗲𝗹 𝘁𝗶𝗱𝗯𝗶𝘁𝘀 & 𝗞𝗼𝗿𝗲𝗮𝗻 𝗲𝗻𝘁𝗲𝗿𝘁𝗮𝗶𝗻𝗺𝗲𝗻𝘁 𝘄𝗵𝗶𝘀𝗽𝗲𝗿𝘀
• 𝗔𝗻𝗱 𝗮𝗹𝗹 𝘁𝗵𝗲 𝘀𝗰𝗮𝗻𝗱𝗮𝗹𝗼𝘂𝘀 𝘁𝗮𝗹𝗲𝘀 𝘁𝗵𝗮𝘁 𝗸𝗲𝗲𝗽 𝘁𝗵𝗶𝘀 𝘄𝗼𝗿𝗹𝗱 𝘁𝘂𝗿𝗻𝗶𝗻𝗴!

✦─────────────────────────✦
➤ 𝗪𝗮𝗻𝘁 𝗺𝗲 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽?
𝗧𝗵𝗲𝗻 𝗿𝗮𝗶𝘀𝗲 𝘁𝗵𝗼𝘀𝗲 𝘂𝗽𝘃𝗼𝘁𝗲𝘀 𝗵𝗶𝗴𝗵!
𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀 𝗮𝗿𝗲𝗻’𝘁 𝘆𝗲𝘁 𝘀𝗲𝘁 𝗶𝗻 𝘀𝘁𝗼𝗻𝗲 — 𝗼𝗻𝗹𝘆 𝘄𝗵𝗲𝗻 𝗲𝗻𝗼𝘂𝗴𝗵 𝘃𝗼𝗶𝗰𝗲𝘀 𝗿𝗶𝘀𝗲
𝘄𝗶𝗹𝗹 𝗜 𝗰𝗵𝗮𝗿𝘁 𝗵𝗼𝘄 𝘁𝗼 𝗯𝗿𝗶𝗻𝗴 𝘁𝗵𝗲 𝗳𝗿𝗲𝘀𝗵𝗲𝘀𝘁 𝗻𝗲𝘄𝘀 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗱𝗼𝗼𝗿𝘀𝘁𝗲𝗽.

✦─────────────────────────✦
𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝗳𝘂𝗲𝗹𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗳𝗹𝗶𝗴𝗵𝘁 —
𝘁𝗼𝗴𝗲𝘁𝗵𝗲𝗿, 𝘄𝗲’𝗹𝗹 𝗲𝗻𝘀𝘂𝗿𝗲 𝗻𝗼 𝘀𝗰𝗼𝗼𝗽 𝗴𝗼𝗲𝘀 𝘂𝗻𝗵𝗲𝗮𝗿𝗱. ❖
"""
    upvote_image_path = os.path.join('IMAGE', 'upvote.jpg')
    
    await query.edit_message_media(
        media=InputMediaPhoto(open(upvote_image_path, 'rb'), caption=caption),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Upvote Now", callback_data="do_upvote")],
            [InlineKeyboardButton("Back", callback_data="about_morgan")]
        ])
    )

async def do_upvote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the actual upvote from the button"""
    query = update.callback_query
    user = update.effective_user
    
    try:
        upvote_data = load_upvotes()
        
        # Initialize users dictionary if not present
        if "users" not in upvote_data:
            upvote_data["users"] = {}
        
        if str(user.id) in upvote_data["users"]:
            # User already voted - show message without trying to edit the same message
            await query.answer("Already Voted - Thanks!", show_alert=True)
            return
        
        # New vote - add user ID and increment count
        upvote_data["users"][str(user.id)] = True
        upvote_data["count"] = upvote_data.get("count", 0) + 1
        
        if save_upvotes(upvote_data):
            await query.answer("✅ Thank you for your upvote!", show_alert=True)
            # Refresh the upvote page to show the new count
            try:
                await show_upvote_page(update, context)
            except Exception as e:
                # If editing fails, just log it - we've already shown the alert
                print(f"Error refreshing upvote page: {e}")
        else:
            await query.answer("❌ Failed to save your upvote. Please try again.", show_alert=True)
    except Exception as e:
        await query.answer("❌ An error occurred. Please try again.", show_alert=True)
        print(f"Error in upvote callback: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    data = query.data
    
    if data == "about_morgan":
        await about_morgan_callback(update, context)
    elif data == "upvote_morgan":
        await show_upvote_page(update, context)
    elif data == "do_upvote":
        await do_upvote_callback(update, context)
    elif data == "main_menu":
        await query.answer("Returning to main...")
        await start_command(update, context)

def get_start_handlers():
    """Return all start-related handlers"""
    return [
        CommandHandler("start", start_command),
        CallbackQueryHandler(button_callback)
    ]