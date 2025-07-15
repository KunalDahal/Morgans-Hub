from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import os

image_path = os.path.join('IMAGE', 'edit.jpg')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = '''
✦───────────────✦
𝗛𝗶 𝘁𝗵𝗲𝗿𝗲! 𝗪𝗵𝗼 𝗮𝗺 𝗜?
𝗜’𝗺 𝗠𝗼𝗿𝗴𝗮𝗻𝘀 — 𝘁𝗵𝗲 𝗯𝗶𝗴, 𝗯𝗼𝗹𝗱 𝗻𝗲𝘄𝘀 𝗯𝗶𝗿𝗱, 𝗽𝗿𝗲𝘀𝗶𝗱𝗲𝗻𝘁 𝗼𝗳 𝗮𝗹𝗹 𝘁𝗵𝗶𝗻𝗴𝘀 𝗻𝗲𝘄𝘀!
𝗧𝗵𝗲𝘆 𝘀𝗮𝘆 𝗜 𝗳𝗹𝗮𝗽 𝗺𝘆 𝘄𝗶𝗻𝗴𝘀 𝗳𝗮𝘀𝘁𝗲𝗿 𝘁𝗵𝗮𝗻 𝗿𝘂𝗺𝗼𝗿𝘀 𝘀𝗽𝗿𝗲𝗮𝗱 𝗮𝗰𝗿𝗼𝘀𝘀 𝘁𝗵𝗲 𝗚𝗿𝗮𝗻𝗱 𝗟𝗶𝗻𝗲.
✦───────────────✦
𝗪𝗮𝗻𝗻𝗮 𝗸𝗻𝗼𝘄 𝗺𝗼𝗿𝗲 𝗮𝗯𝗼𝘂𝘁 𝗺𝘆 𝘀𝗲𝗰𝗿𝗲𝘁 𝘀𝗰𝗼𝗼𝗽𝘀, 𝘄𝗶𝗹𝗱 𝗵𝗲𝗮𝗱𝗹𝗶𝗻𝗲𝘀,
𝗼𝗿 𝗵𝗼𝘄 𝗺𝗮𝗻𝘆 𝗯𝗲𝗿𝗿𝗶𝗲𝘀 𝗜 𝘀𝗽𝗲𝗻𝗱 𝗼𝗻 𝗺𝘆 𝘁𝗼𝗽 𝗵𝗮𝘁𝘀?
𝗝𝘂𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗺𝗲 𝗼𝗻 𝗺𝘆 𝗼𝘁𝗵𝗲𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁:@MorgansNews_Bot!
✦───────────────✦
𝗣𝗲𝗮𝗰𝗲... 𝗮𝗻𝗱 𝗿𝗲𝗺𝗲𝗺𝗯𝗲𝗿:
𝗶𝗳 𝗶𝘁’𝘀 𝗻𝗲𝘄𝘀𝘄𝗼𝗿𝘁𝗵𝘆, 𝗜’𝗺 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝘀𝗾𝘂𝗮𝘄𝗸𝗶𝗻𝗴 𝗮𝗯𝗼𝘂𝘁 𝗶𝘁! 
'''
    await update.message.reply_photo(
        photo=image_path,  
        caption=message)
   

def get_start_handler():
    return CommandHandler("start", start_command)
