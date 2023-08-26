# installing packedges
from telebot.types import Message

# local variables and functions
from loader import bot


@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id # requesting user
    # send message to requesting user
    bot.send_message(chat_id, f"Assalomu Aleykum {message.from_user.first_name}, Your Chat ID: {chat_id}")


@bot.message_handler(commands=["help"])
def help(message: Message):
    """ help command """
    chat_id = message.chat.id # request.user
    bot.send_message(chat_id, "Yordam uchun @turgunovzohidillo ga yozing")
