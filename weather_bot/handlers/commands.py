from telebot.types import Message

from bot import bot
from keyboards import start_btn


@bot.message_handler(commands=["start"])
def start(message: Message):
    """ start command return hello """
    user = message.chat.id
    bot.send_message(
        user, f"Asslomu Alykum {message.from_user.first_name}\nOb-havo botiga hush kelibsiz!",
        reply_markup=start_btn()
    )