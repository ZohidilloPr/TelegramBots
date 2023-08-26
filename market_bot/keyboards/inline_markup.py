from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.loader import db



def help_btn():
    markub = InlineKeyboardMarkup()
    markub.add(InlineKeyboardButton("dasturchi", url="https://t.me/ZohidilloTurgunov/"))
    return markub


def groups_list():
    markup = InlineKeyboardMarkup()
    groups = db.get_all_groups()
    for g in groups:
        markup.row(
            InlineKeyboardButton(text=g[2], callback_data=f"groups|{g[1]}")
        )
    return markup