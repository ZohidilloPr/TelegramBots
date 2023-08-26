from telebot.types import (CallbackQuery, InputFile, CallbackQuery)


from config import *
from loader import db, bot


def requared_admin(func):
    def methods(call: CallbackQuery):
        group_admins = bot.get_chat_administrators(GROUP_CHAT_ID)
        admins = [item.user.id for item in group_admins]
        if call.from_user.id in admins:
            func(call)
        else:
            bot.send_message(call.chat.id, "Bu buyruqlar faqat adminlar uchun")
    return methods


@requared_admin
@bot.callback_query_handler(func=lambda call: "quarter" in call.data)
def reaction_quarter(call: CallbackQuery):
    chat_id = call.message.chat.id
    quarter = int(call.data.split("|")[1])
    if quarter != 5:
        file = InputFile(db.get_quarterly_messages(quarter))
        caption = f"{quarter}-Choraklik muroajatlar hisoboti"
        bot.send_document(chat_id=chat_id, document=file, caption=caption)

