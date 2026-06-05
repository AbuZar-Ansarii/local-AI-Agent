from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from config.settings import TELEGRAM_BOT_TOKEN
from .handlers import start_command, help_command, clear_command, handle_message, handle_voice, screenshot_command

logger = logging.getLogger(__name__)

def create_bot():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("No Telegram Bot Token provided in settings.")
        return None
        
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("screenshot", screenshot_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Voice
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    return application
