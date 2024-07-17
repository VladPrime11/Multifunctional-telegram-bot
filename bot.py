# bot.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import TELEGRAM_TOKEN
from handlers.weather_handler import weather, toggle_weather, back_to_main, send_weather_notifications
from handlers.settings_handler import settings
from utils.logger import setup_logger
from utils.state_manager import StateManager

logger = setup_logger(__name__)
state_manager = StateManager()


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [['🌤️ Погода', '⚙️ Настройки']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    logger.info("Starting bot")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text(['🌤️ Погода']), weather))
    application.add_handler(MessageHandler(filters.Text(['⚙️ Настройки']), settings))
    application.add_handler(MessageHandler(filters.Text(['🔔 Включить погоду: ON']), toggle_weather))
    application.add_handler(MessageHandler(filters.Text(['🔔 Включить погоду: OFF']), toggle_weather))
    application.add_handler(MessageHandler(filters.Text(['🔙 Назад']), back_to_main))

    application.run_polling()


if __name__ == '__main__':
    main()
