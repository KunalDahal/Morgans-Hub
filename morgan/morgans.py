import os
import logging
from telegram.ext import Application
from telegram import Update
from dotenv import load_dotenv
from util import get_bot_token
from morgan.commands.start import get_start_handlers
from morgan.commands.upvote import get_upvote_handlers
from morgan.commands.request import get_request_handler
from morgan.commands.approve import get_approve_handler
from morgan.edit.edit import get_edit_admin_handler
from morgan.admin import get_morgans_ids
import asyncio
from telegram import BotCommandScopeDefault, BotCommandScopeChat

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Post initialization function to set bot commands based on user status"""
    public_commands = [
        ("start", "Start the bot"),
    ]

    admin_commands = public_commands + [
        ("edit", "Formats post; translates Italian/Russian to English if used [it|ru]"),
        ("start", "Start the bot")
    ]

    await application.bot.set_my_commands(
        public_commands, scope=BotCommandScopeDefault()
    )

    for admin_id in get_morgans_ids():
        await application.bot.set_my_commands(
            admin_commands, scope=BotCommandScopeChat(admin_id)
        )

def main() -> None:
    application = (
        Application.builder().token(get_bot_token()).post_init(post_init).build()
    )

    for handler in get_start_handlers():
        application.add_handler(handler)

    for handler in get_upvote_handlers():
        application.add_handler(handler)

    application.add_handler(get_request_handler())
    application.add_handler(get_approve_handler())
    application.add_handler(get_edit_admin_handler())

    async def run_bot():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        # Keep the bot running
        await asyncio.Event().wait()

    logger.info("Starting bot...")
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()