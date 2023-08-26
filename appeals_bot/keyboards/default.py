# --- Buttons for users ---

# --- Importing from libraries ---

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


# --- The end of Importing from libraries ---


# --- Ro'yxatdan otish 📄 (register) button ---

def register():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Ro'yxatdan otish 📄")
    )
    return markup


# --- The end of Ro'yxatdan otish 📄 (register) button ---


# --- Murojaat yuborish ✍️ (user_message) button ---

def user_message():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Murojaat yuborish ✍️")
    )
    return markup


# --- The end of Murojaat yuborish ✍️ (user_message) button ---


# --- Gender button ---

def gender():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("Erkak"),
        KeyboardButton("Ayol")
    )
    return markup


# --- The end of Gender button ---


# --- Share contact button ---

def share_contact():
    contact_button = KeyboardButton("👉Raqamni yuborish👈", request_contact=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(contact_button)
    return markup


# --- The end of Share contact button ---


# --- City button ---

def city():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    regions = db.get_all_regions_name()

    for i in range(0, len(regions), 2):
        if i + 1 < len(regions):
            markup.add(
                KeyboardButton(regions[i]),
                KeyboardButton(regions[i + 1])
            )
        else:
            markup.add(
                KeyboardButton(regions[i])
            )

    return markup


# --- The end of City button ---


# --- register_submit_btn button ---

def register_submit_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Ha"),
        KeyboardButton("Yo'q")
    )
    return markup


# --- The end of register_submit_btn button ---


# --- Problem_type button ---

def problem_type(appeals_type_name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons_row = []
    for item in db.get_problem_types_by_appeals_type(appeals_type_name):
        button = KeyboardButton(item)
        buttons_row.append(button)
        if len(buttons_row) == 2:
            markup.row(
                *buttons_row
            )
            buttons_row = []
    if buttons_row:
        markup.row(*buttons_row)
    return markup


# --- The end of Problem_type button ---


def DocumentsYes():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    document_types = [KeyboardButton("Hujjat 📄"), KeyboardButton("Foto rasm 📷"), KeyboardButton("Video fayl 🎥")]
    markup.row(*document_types)
    markup.add(KeyboardButton("Mavjud emas 🚫"))
    return markup


def send_appeals_btn():
    """ murojatni yuborish uchun  """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    return markup.add(KeyboardButton("Yuborish ✅"),
                      KeyboardButton("Bekor qilish ❌"))

# --- The end of Buttons for users ---



# --- Buttons for ADMINS ---


def admin_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('Foydalanuvchilar soni'),
        KeyboardButton("Habar yuborish"),
        KeyboardButton("Muammo turini qo'shish"),
        KeyboardButton("Muammo turini o'chirish"),
        KeyboardButton("Hisobot"),
        KeyboardButton("Foydalanuvchining barcha murojatlarni ko'rish"),
    )
    return markup


def hisobot_type_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('Haftalik'),
        KeyboardButton('Oylik'),
        KeyboardButton('Chorak'),
        KeyboardButton('Yil'),
        KeyboardButton('Orqaga qaytish')
    )
    return markup


def go_back_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton('Orqaga qaytish')
    )
    return markup


def appeals_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in db.get_all_appeals_type_name():
        markup.add(KeyboardButton(item))
    return markup


def to_excel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Ma'lumotlarni excel faylda yuklab olish"), 
        KeyboardButton('Orqaga qaytish')
    )
    return markup
