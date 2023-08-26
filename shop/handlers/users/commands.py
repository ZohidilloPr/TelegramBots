from telebot.types import Message

from loader import bot, db
from keyboards.inline_murkup import help_btn
from keyboards.replay_murkup import start_btn, register_btn

@bot.message_handler(commands=["start", "help"])
def start(message: Message):    
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "/start":
        check = db.check_user_in_db(telegram_id=user_id)
        if check:
            bot.send_message(chat_id, f"Assalomu Aleykum {message.from_user.first_name}\nOnline Marketga xush kelibsiz!", reply_markup=start_btn())
        else: 
            bot.send_message(chat_id, "Ro'yhatdan o'tishingiz kerak", reply_markup=register_btn())
    elif message.text == "/help":
        bot.send_message(chat_id, f"Bot nosozligi bo'yicha xabar berish uchun yozing.", reply_markup=help_btn())


# @bot.message_handler(commands=["clear"])
# def clear_history(message: Message):
#     chat_id = message.chat.id
#     user_id = message.from_user.id

#     # Get a list of message IDs sent by the bot to the user
#     message_ids = db.get_user_message_ids(telegram_id=user_id)

#     # Delete each message from the chat
#     for message_id in message_ids:
#         bot.delete_message(chat_id, message_id)

#     # Clear the user's message history in the database
#     db.clear_user_message_history(telegram_id=user_id)

#     bot.send_message(chat_id, "Chat history has been cleared.")
