# --- Importing from libraries ---

from telebot.types import Message

# --- The end of Importing from libraries ---


# --- Importing from other folders ---

from loader import bot, db
from keyboards.default import *
from config import GROUP_CHAT_ID
from keyboards.inline import help_btn


# --- The end of Importing from other folders ---


# --- /start and /help button commands ---
@bot.message_handler(commands=['start', 'my_appeals', "my_id"])
def reaction_commands(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id > 0:
        if message.text == '/start':
            print("UserID", chat_id)
            check = db.check_user(user_id)
            group_admins = bot.get_chat_administrators(GROUP_CHAT_ID)
            admins = [item.user.id for item in group_admins]
            if chat_id in admins:
                bot.send_message(chat_id, "Assalomu Alaykum ADMIN", reply_markup=admin_btn())
            elif check:
                bot.send_message(chat_id, f"Assalomu Alaykum {message.from_user.first_name}👋\n"
                                        f"Siz bu bot orqali Toshkent viloyati hokimiga murojaat yuborishingiz mumkin\n"
                                        f"Buning uchun Murojaat yuborish ✍️ tugmasini bosing",
                                reply_markup=user_message())
            else:
                bot.send_message(chat_id, f"Assalomu Alaykum {message.from_user.first_name}👋\n"
                                        f"Siz bu bot orqali Toshkent viloyati hokimiga murojaat yuborishingiz mumkin\n"
                                        f"Buning uchun Ro'yxatdan otish 📄 tugmasini bosing",
                                reply_markup=register())
        # elif message.text == '/help':
        #     bot.send_message(chat_id, f"Agar bot bilan bog'liq muammolarga yuz kelsangiz, iltimos, bizga habar bering!",
        #                     reply_markup=help_btn())
        elif message.text == '/my_appeals':
            check = db.check_user(user_id)
            if check:
                messages = db.user_message(user_id)
                if messages:
                    for message in messages:
                        problem_type = db.get_problem_type_name_by_id(id=int(message[0]))
                        full_message = message[1]
                        register_time = message[5]
                        register_time_formatted = register_time.strftime("%Y-%m-%d %H:%M")
                        if message[2] != " ":  # for document_id
                            bot.send_document(
                                chat_id=chat_id,
                                document=message[2], 
                                caption=f"⬆️ <b>Siz yuborgan hujjat</b> ⬆️\n\n<b>Muammo turi:</b> {problem_type}\n\n<b>To'liq murojaat matni:</b> {full_message}\n\n<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}\n\n", parse_mode='html'
                            )
                        elif message[3] != " ":  # for photo
                            bot.send_photo(
                                chat_id,
                                photo=message[3],
                                caption=f"⬆️ <b>Siz yuborgan rasm</b> ⬆️\n\n<b>Muammo turi:</b> {problem_type}\n\n<b>To'liq murojaat matni:</b> {full_message}\n\n<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}\n\n", parse_mode='html'
                            )
                        elif message[4] != " ":  # for video
                            bot.send_video(
                                chat_id, 
                                video=message[4],
                                caption=f"⬆️ <b>Siz yuborgan rasm</b> ⬆️\n\n<b>Muammo turi:</b> {problem_type}\n\n<b>To'liq murojaat matni:</b> {full_message}\n\n<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}\n\n", parse_mode='html'
                            )
                        else:
                            bot.send_message(chat_id, f"<b>Qo'shimcha hujjatlar:</b> Mavjud emas\n\n<b>Muammo turi:</b> {problem_type}\n\n<b>To'liq murojaat matni:</b> {full_message}\n\n<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}\n\n", parse_mode='html'),
                else:
                    bot.send_message(chat_id, "Siz hali hech qanday murojaat yubormagansiz!\n"
                                      "Murojaat yuborish uchun /start buyrug'ini bosing")
            else:
                bot.send_message(chat_id, "Sizda ro'yxatdan o'tmagansiz! ")
    elif message.text == "/my_id":
        bot.send_message(chat_id, f"Your Chat Id: {chat_id}")

# --- The end of /start and /help button commands ---
