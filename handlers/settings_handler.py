# handlers/settings_handler.py

from telegram import Update
from telegram.ext import CallbackContext

async def settings(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Настройки пока недоступны.")
