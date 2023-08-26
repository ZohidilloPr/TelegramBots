from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

# local variables
from .database import Database
from .settings import (TOKEN, DB_NAME, DB_USER, DB_PASS, DB_HOST) 

# settings bot
bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filters.StateFilter(bot))

# settings database
db = Database(DB_NAME, DB_USER, DB_PASS, DB_HOST)

# commands menu for users
bot.set_my_commands(commands=[
    BotCommand("start", "Botni qayta ishga tushirish"),
    BotCommand("help", "Yordam"),
    BotCommand("my_chat_id", "Chat ID ni aniqlash."),
    # your commands for menu
])
