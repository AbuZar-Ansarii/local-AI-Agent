import logging
import colorlog
from config.settings import LOG_LEVEL
from telegram.bot import create_bot
import asyncio
from android.shizuku import shizuku

def setup_logging():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        handlers=[handler]
    )

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    logger.info("Starting Android Local AI Agent...")
    
    # Check Shizuku status
    if shizuku.is_available():
        logger.info("Shizuku is available and running.")
    else:
        logger.warning("Shizuku is NOT available. Many privileged features will fail.")
        
    bot_app = create_bot()
    if bot_app:
        logger.info("Starting Telegram polling...")
        bot_app.run_polling()
    else:
        logger.error("Failed to start bot application.")

if __name__ == "__main__":
    main()
