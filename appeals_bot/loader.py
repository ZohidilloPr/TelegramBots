# --- Importing from libraries ---

from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

# --- The end of Importing from libraries ---


# --- Importing from other folders ---

from config import *
from database import DataBase

# --- The end of Importing from other folders --


bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.ChatFilter())

db = DataBase(DB_NAME, DB_PASSWORD, DB_HOST, DB_USER)

bot.set_my_commands(commands=[
    BotCommand('start', 'Bot-ni qayta ishga tushirish'),
    BotCommand('my_appeals', "Mening murojaatlarim")
])
