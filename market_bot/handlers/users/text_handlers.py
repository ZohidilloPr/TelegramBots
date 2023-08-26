from telebot.types import Message

# local variables
from config.loader import bot, db

@bot.message_handler(content_types=["text"])
def reaction_salom(message: Message):
    print("data")
    group = db.get_all_public_groups()[0]
    bot.send_message(chat_id=group, text="123456")