from telebot.handler_backends import State, StatesGroup

class WeatherState(StatesGroup):
    weather = State()