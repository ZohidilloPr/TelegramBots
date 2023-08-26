from telebot.types import Message

from bot import bot
from keyboards.replayMarkup import start_btn


@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, 
        f"Assalomu Aleykum {message.from_user.first_name}\nMen tarjimon botman :)",
        reply_markup=start_btn()) 