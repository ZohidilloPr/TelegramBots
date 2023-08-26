# --- Importing from libraries ---

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default import admin_btn


# --- The end of Importing from libraries ---


# --- /help inline button ---

def help_btn():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Muammo haqida xabar berish", url='https://t.me/PFNTDY'))
    return markup

# --- The end of /help inline button ---


# --- Murojaat yuborish ✍️utton ---

def murojaat_yuborish(user_message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Murojaat yuborish ✍️", callback_data=user_message))
    return markup

# --- The end of Murojaat yuborish ✍️ inline button ---


# --- The end of Javob berish ✍️ inline button ---

def javob_berish(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Javob yozish ✍️", callback_data=f"write_response|{user_id}")
        )
    return markup



def quarter_btn():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("1-chorak", callback_data="quarter|1"),
        InlineKeyboardButton("2-chorak", callback_data="quarter|2"),
        InlineKeyboardButton("3-chorak", callback_data="quarter|3"),
        InlineKeyboardButton("4-chorak", callback_data="quarter|4"),
    )
    return markup
# --- The end of Javob berish ✍️ inline button ---
