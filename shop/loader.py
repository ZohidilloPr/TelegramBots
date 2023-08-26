from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from config import *
from database import Database


bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.set_my_commands(commands=[
    BotCommand("start", "Botni qayta ishga tushurish"),
    BotCommand("help", "Yordam uchun"),
    # BotCommand("clear", "clear chat")
])
db = Database(DB_NAME, DB_PASSWORD, DB_HOST, DB_USER)