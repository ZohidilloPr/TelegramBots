from telebot.types import Message

# local variables
from config.loader import bot, db
from keyboards.relpy_markup import home_btn
from keyboards.inline_markup import help_btn


# start coding
@bot.message_handler(commands=["start", "help", "my_chat_id"])
def reaction_commands(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    ADMIN = []
    admins = bot.get_chat_administrators(-1001984280958)
    if chat_id > 0:
        if message.text == "/start":
            for admin in admins:
                db.set_admins(admin.user.id)
            ADMINS = db.get_admins_telegram_id()
            check = db.check_user_exists(user_id)
            if check:
                if user_id in ADMINS:
                    bot.send_message(chat_id, "Assalom Aleykum Admin", reply_markup=home_btn())
                elif user_id not in ADMINS:
                    bot.send_message(chat_id, "Assalom Aleykum Market Bot ishga tushdi.")
            else:
                telegram_id = int(user_id)
                f_name = message.from_user.first_name
                l_name = message.from_user.last_name
                username = message.from_user.username
                db.insert_users_table(telegram_id, f_name, l_name, username)
                bot.send_message(chat_id, "Assalomu Alykum Market Bot ishga tushdi.")
        elif message.text == "/help":
            bot.send_message(chat_id, "Dasturchi bilan bog'lanish", reply_markup=help_btn())
    elif message.text == "/my_chat_id":
        bot.send_message(chat_id, f"My Chat ID: {chat_id}")
    else:
        chat_info = bot.get_chat(chat_id)
        group = {
            "chat_id": chat_id,
            "user_name": chat_info.username,
            "public": False
        }
        db.insert_group_table(**group)
