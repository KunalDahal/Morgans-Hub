import os
import logging
from telegram.ext import Application
from telegram import Update
from dotenv import load_dotenv
from util import get_bot_token
from morgan.start import get_start_handlers
from morgan.upvote import get_upvote_handlers
from morgan.request import get_request_handler
from morgan.approve import get_approve_handler

load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Optional post-initialization tasks"""
    await application.bot.set_my_commands([
        ("start", "Start the bot for info")
    ])

def main() -> None:
    """Run the bot"""
    # Create Application
    application = Application.builder().token(get_bot_token()).post_init(post_init).build()

    # Add handlers
    for handler in get_start_handlers():
        application.add_handler(handler)
    
    # Add upvote handlers
    for handler in get_upvote_handlers():
        application.add_handler(handler)
    
    application.add_handler(get_request_handler())
    application.add_handler(get_approve_handler())

    # Run bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()