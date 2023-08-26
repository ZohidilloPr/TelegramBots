from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_btn():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    murkup.row(KeyboardButton("Tarjima"), KeyboardButton("Wikipidea"))
    return murkup