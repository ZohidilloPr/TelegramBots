from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from config import TOKEN


bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filters.StateFilter(bot))