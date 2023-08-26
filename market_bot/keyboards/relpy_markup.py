from telebot.types import ReplyKeyboardMarkup, KeyboardButton


from config.loader import db


def home_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton("Maxsulot qo'shish"),
        KeyboardButton("Botga bog'langan Guruxlar")
    )
    return markup


def categories_list():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in db.get_all_categories_name():
        markup.add(KeyboardButton(item))
    return markup


def example_sizes(product_pk=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    sizes = db.get_all_example_sizes_name(product_pk)
    for item in sizes:
        markup.add(KeyboardButton(item))
    return markup


def yes_no():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Ha"), KeyboardButton("Yoq"))
    return markup
    

def example_colors(product_pk:None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    colors = db.get_all_example_colors_name(product_pk)
    for item in colors:
        markup.add(KeyboardButton(item))
    return markup
    

def old_data(data):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(data))
    return markup


