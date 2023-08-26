from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_btn():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    murkup.add(
        KeyboardButton("Menu 🛍"),
        KeyboardButton("Savat 🛒"),
        KeyboardButton("Sozlamalar ⚙️"),
        KeyboardButton("Qayta aloqa 📞")
    )
    return murkup


def register_btn():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    murkup.add(KeyboardButton("Ro'yhatdan o'tish ✍️"))
    return murkup


def share_contact():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    murkup.add(KeyboardButton("Raqamni ulashish", request_contact=True))
    return murkup


def register_submit_btn():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    murkup.row(KeyboardButton("Ha"), KeyboardButton("Yoq"))
    return murkup


def catgories_btn(categories_list: list):
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories_list:
        murkup.add(KeyboardButton(category))
    murkup.add(KeyboardButton("Asosiy Menu  🔙"))
    return murkup