import requests
from datetime import datetime
from telebot.types import Message, ReplyKeyboardRemove

from bot import bot
from states import WeatherState
from config import WEATHER_API_KEY
from keyboards import start_btn, RegionsBTN


@bot.message_handler(regexp="Ob-Havo")
def reaction_weather(message: Message):
    user = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, WeatherState.weather, user)
    bot.send_message(
        user, "Qaysi hududni Ob-havosini bilmoqchisiz ?",
        reply_markup=RegionsBTN())


@bot.message_handler(content_types=["text"], state=WeatherState.weather)
def get_weather(message: Message):
    user = message.chat.id
    user_id = message.from_user.id
    url = f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        country = data["sys"]["country"]
        wind = data["wind"]["speed"]
        timezone = data["timezone"]
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + timezone).strftime("%d-%m-%Y %H:%M:%S")
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + timezone).strftime("%d-%m-%Y %H:%M:%S")
        temp = round(int(data["main"]["temp"]) - 273.15, 2)
        final_data = f"""
            {message.text.capitalize()}da Ob-Havo:
            Temperatura: {temp} °C
            Shamol tezligi: {wind} m/s
            Respublika qisqa kodi: {country}
            Quyosh chiqishi: {sunrise}
            Quyosh botishi: {sunset} 
        """
        bot.send_message(user, final_data, reply_markup=start_btn())
        bot.delete_state(user_id, user)
    else:
        bot.send_message(user, "Shaxar nomida xatolik bo'lishi mumkun", reply_markup=start_btn())
        bot.delete_state(user_id, user) 
