# handlers/weather_handler.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import WEATHER_API_KEY, CITY_NAME
from services.weather_service import WeatherService
from utils.state_manager import StateManager
from datetime import time, datetime

weather_service = WeatherService(WEATHER_API_KEY, CITY_NAME)
state_manager = StateManager()


async def weather(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    state = state_manager.get_state(user_id)
    keyboard = [[f'🔔 Включить погоду: {state}', '🔙 Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Настройки погоды:', reply_markup=reply_markup)


async def toggle_weather(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    current_state = state_manager.get_state(user_id)
    new_state = 'OFF' if current_state == 'ON' else 'ON'
    state_manager.set_state(user_id, new_state)

    if new_state == 'ON':
        context.job_queue.run_daily(send_weather_notifications, time(hour=9, minute=0), data=update.message.chat_id)
        await update.message.reply_text('Уведомления о погоде включены.')
    else:
        for job in context.job_queue.jobs():
            job.schedule_removal()
        await update.message.reply_text('Уведомления о погоде отключены.')

    keyboard = [[f'🔔 Включить погоду: {new_state}', '🔙 Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Настройки погоды:', reply_markup=reply_markup)


async def back_to_main(update: Update, context: CallbackContext) -> None:
    keyboard = [['🌤️ Погода', '⚙️ Настройки']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)


async def send_weather_notifications(context: CallbackContext):
    chat_id = context.job.data
    weather_data = weather_service.get_weather()
    if weather_data:
        today = datetime.now().date()
        daily_temperatures = [entry['main']['temp'] for entry in weather_data['list'] if
                              datetime.fromtimestamp(entry['dt']).date() == today]
        daily_max = max(daily_temperatures)
        daily_min = min(daily_temperatures)

        message = (
            f"🌤️ Погода в {CITY_NAME}:\n"
            f"🌡️ Текущая температура: {weather_data['list'][0]['main']['temp']}°C\n"
            f"📈 Максимальная температура за день: {daily_max}°C\n"
            f"📉 Минимальная температура за день: {daily_min}°C\n"
            f"☁️ Погода: {weather_data['list'][0]['weather'][0]['description']}\n"
            f"💧 Влажность: {weather_data['list'][0]['main']['humidity']}%\n"
            f"💨 Скорость ветра: {weather_data['list'][0]['wind']['speed']} м/с"
        )
        await context.bot.send_message(chat_id, text=message)
    else:
        await context.bot.send_message(chat_id, text=f"Не удалось получить данные о погоде для {CITY_NAME}.")
