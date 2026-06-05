from telegram import Update
from telegram.ext import ContextTypes
import logging
from config.settings import ALLOWED_USER_IDS
from agent.graph import app as agent_app
from agent.memory import short_term_memory
from langchain_core.messages import HumanMessage
import asyncio
import os

logger = logging.getLogger(__name__)

async def check_auth(update: Update) -> bool:
    user_id = update.effective_user.id
    if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
        logger.warning(f"Unauthorized access attempt from user {user_id}")
        await update.message.reply_text("Unauthorized access.")
        return False
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("Hello! I am your Android Local AI Agent. Send me commands!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    help_text = """
    *Commands:*
    /start - Start the bot
    /help - Show this message
    /clear - Clear short-term memory
    /screenshot - Take a screenshot and send it
    
    You can also just send me natural language commands like:
    "Open YouTube", "Turn on WiFi", "What is my battery level?"
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    user_id = update.effective_user.id
    short_term_memory.clear(user_id)
    await update.message.reply_text("Short-term memory cleared.")

async def screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("Taking screenshot...")
    from android.shizuku import shizuku
    import time
    
    filepath = "/sdcard/telegram_screenshot.png"
    shizuku.take_screenshot(filepath)
    
    # Wait a moment for file write
    await asyncio.sleep(1)
    
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            await update.message.reply_photo(photo=f)
        os.remove(filepath)
    else:
        await update.message.reply_text("Failed to capture screenshot.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    
    user_message = update.message.text
    user_id = update.effective_user.id
    
    if not user_message:
        return
        
    logger.info(f"Received message from {user_id}: {user_message}")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Update short term memory
    short_term_memory.add_message(user_id, HumanMessage(content=user_message))
    history = short_term_memory.get_history(user_id)
    
    try:
        # Run agent
        result = agent_app.invoke({
            "messages": history,
            "user_id": user_id,
            "context": "",
            "errors": [],
            "next_step": ""
        })
        
        final_message = result["messages"][-1]
        
        # Add AI response to memory
        short_term_memory.add_message(user_id, final_message)
        
        # Send response
        await update.message.reply_text(final_message.content)
        
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        await update.message.reply_text(f"An error occurred while processing your request: {str(e)}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("Voice support is not fully implemented yet. Please use text.")
    # Here you would download the voice file, run Faster Whisper, and feed text to handle_message
