# --- Importing from libraries ---

from datetime import datetime
from telebot.types import (
    Message, 
    KeyboardButton, 
    ReplyKeyboardRemove, 
    ReplyKeyboardMarkup
)

from keyboards.default import (
    gender, share_contact, city,
    register_submit_btn, problem_type, DocumentsYes, send_appeals_btn, appeals_type
)

# --- The end of Importing from libraries ---


# --- Importing from other folders ---

from loader import *
from states import *
from config import ADMINS

# --- The end of Importing from other folders ---


@bot.message_handler(regexp="Murojaat yuborish ✍️")
def reaction_appeals(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, MessageStates.appeals_type, chat_id)
    bot.send_message(chat_id, "Iltimos qanday murojat ekanligini tanlang!", reply_markup=appeals_type())


@bot.message_handler(content_types=["text"], state=MessageStates.appeals_type)
def reaction_appeals_type(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    appeals_type = message.text
    if appeals_type in db.get_all_appeals_type_name():
        with bot.retrieve_data(user_id, chat_id) as data:
            data["appeals_type_id"], data["appeals_type"] = db.get_appeals_id_by_appeal_type_name(appeals_type), appeals_type
            bot.set_state(user_id, MessageStates.user_problem_type, chat_id)
            bot.send_message(chat_id, "Iltimos muommo turini tanlang!", reply_markup=problem_type(appeals_type))
    else:
        bot.set_state(user_id, MessageStates.appeals_type, chat_id)
        bot.send_message(chat_id, "Iltimos pastda ko'rsatilgan tugmalardan foydalaning!", reply_markup=appeals_type())


@bot.message_handler(content_types=["text"], state=MessageStates.user_problem_type)
def reaction_problem_type(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text in db.get_all_problem_types():
        with bot.retrieve_data(user_id, chat_id) as data:
            data["document_id"], data["photo_id"], data["video_id"] = " ", " ", " "
            data["problem_type"], data["problem_type_name"] = db.get_problem_type_id_by_name(message.text), message.text
            bot.set_state(user_id, MessageStates.user_message, chat_id)
            bot.send_message(chat_id, "Murojatingizni to'liq shaklini yozing", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Faqat ko'rsatilgan muammo turlaridan birini tanlang!")


@bot.message_handler(content_types=["text"], state=MessageStates.user_message)
def reaction_user_message(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data["user_message"] = message.text.replace("'", "`")
        bot.set_state(user_id, MessageStates.yes_or_no, chat_id)
        bot.send_message(
            chat_id,
            "Murojatingizga aloqador biron bir qo'shimcha hujjat, rasm yoki video bor bo'lsa pastagi tugmalar orqali yuboring yoki 'Mavjud emas' degan tugmani bo'sing.",
            reply_markup=DocumentsYes()
        )


@bot.message_handler(content_types=["text"], state=MessageStates.yes_or_no)
def reaction_yes_or_no(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.text == "Mavjud emas 🚫":
            data["yes_or_no"] = False
            bot.set_state(user_id, MessageStates.submit, chat_id)
            bot.send_message(chat_id, f"""Murojaatingiz yuborish uchun tayyor!\n
<b>Murojaat Yuboruvchi:</b> {data["appeals_type"]}
<b>Murojaat turi:</b> {data['problem_type_name']}
<b>Murojaatning to'liq shakli:</b>\n{data['user_message']}
<b>Qo'shimcha hujjatlar:</b> Mavjud emas""", parse_mode='html', reply_markup=send_appeals_btn())
        elif message.text == "Hujjat 📄":
            bot.set_state(user_id, MessageStates.document_id, chat_id)
            bot.send_message(chat_id, "Iltimos hujjatni yuboring!", reply_markup=ReplyKeyboardRemove())
        elif message.text == "Foto rasm 📷":
            bot.set_state(user_id, MessageStates.photo_id, chat_id)
            bot.send_message(chat_id, f"Iltimos rasmni yuboring!", reply_markup=ReplyKeyboardRemove())
        elif message.text == "Video fayl 🎥":
            bot.set_state(user_id, MessageStates.video_id, chat_id)
            bot.send_message(chat_id, "Iltimos videoni yuboring!", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"], state=MessageStates.submit)
def reaction_submit(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "Yuborish ✅":
        with bot.retrieve_data(user_id, chat_id) as data:
            user = db.get_user_from_telegram_id(user_id)
            send_data = {
                "user": db.get_user_id_from_telegram_id(user_id),
                "appeals_type_id": data["appeals_type_id"],
                "problem_type": data["problem_type"],
                "user_message": data["user_message"],
                "document_id": data["document_id"],
                "photo_id": data["photo_id"],
                "video_id": data["video_id"]
            }

            db.insert_messages_table(**send_data)
            def send_messages_to_group(admin_chat_id, data, user):
                user_message = data['user_message']
                caption = f"""⬆️ Foydalanuvchi yuborgan qo'shimcha hujjat ⬆️
\nℹ️ Yangi murojaat ! ℹ️
<b>user_id:</b> |{user[1]}|
<b>To'liq ismi:</b> {user[2].title()}
<b>Jinsi:</b> {user[3].capitalize()}
<b>Tug'ilgan kuni:</b> {user[4]}
<b>Telefon raqami::</b> {user[6]} ✅
<b>Tuman/shahar:</b> {user[7]}
<b>Mahalla va manzili:</b> {user[8]}
<b>Muammo turi:</b> {data['problem_type_name']}
<b>Murojaatning to'liq shakli:</b>\n {user_message}"""
                if len(caption) >= 1024:
                    caption_0 = caption[:1020] + "..."
                    caption_1 = caption[1020:] + f"\n<b>user_id:</b> |{user[1]}|"
                    if data["document_id"] != " ":
                        bot.send_document(chat_id=admin_chat_id, document=data["document_id"], caption=caption_0, parse_mode='html')
                        bot.send_message(chat_id=admin_chat_id, text=caption_1, parse_mode="HTML")
                    
                    elif data["photo_id"] != " ":
                        bot.send_photo(chat_id=admin_chat_id, photo=data["photo_id"], caption=caption_0, parse_mode='html')
                        bot.send_message(chat_id=admin_chat_id, text=caption_1, parse_mode="HTML")

                    elif data["video_id"] != " ":
                        bot.send_video(chat_id=admin_chat_id, video=data["video_id"], caption=caption_0, parse_mode='html')
                        bot.send_message(chat_id=admin_chat_id, text=caption_1, parse_mode="HTML")

                    else:
                        bot.send_message(chat_id=admin_chat_id, text=f"Foydalanuvchi hech qanday qo'shimcha hujjat yubormadi \n {caption}", parse_mode='html')
                else:
                    if data["document_id"] != " ":
                        bot.send_document(chat_id=admin_chat_id, document=data["document_id"], caption=caption, parse_mode='html')
                        
                    elif data["photo_id"] != " ":
                        bot.send_photo(chat_id=admin_chat_id, photo=data["photo_id"], caption=caption, parse_mode='html')
                        
                    elif data["video_id"] != " ":
                        bot.send_video(chat_id=admin_chat_id, video=data["video_id"], caption=caption, parse_mode='html')
                        
                    else:
                        bot.send_message(chat_id=admin_chat_id, text=f"Foydalanuvchi hech qanday qo'shimcha hujjat yubormadi \n {caption}", parse_mode='html')

            import re
            for admin_chat_id in GROUPS:
                if re.search("adbirkor", data["appeals_type"]):
                    send_messages_to_group(GROUPS.get("tadbirkor"), data, user)
                    break
                elif re.search("uqo", data["appeals_type"]):
                    send_messages_to_group(GROUPS.get("fuqoro"), data, user)
                    break
            bot.send_message(
                chat_id,
                "Murojaatingiz yuborildi. Murojaatingizga 15 ish kunidan 30 ish kunigacha bo'lgan muddat davomida javob beriladi."
                "\nYangi murojaat yozish uchun /start buyrugʻiga bosing",
                reply_markup=ReplyKeyboardRemove()
            )

    elif message.text == "Bekor qilish ❌":
        with bot.retrieve_data(user_id, chat_id) as data:
            data.clear()
        bot.send_message(
            chat_id, 
            "Murojaat bekor qilindi! Yangi murojaat yozish uchun /start buyrugʻiga bosing",
            reply_markup=ReplyKeyboardRemove()
        )
        

'''File-ni qismi'''


@bot.message_handler(content_types=["document"], state=MessageStates.document_id)
def reaction_document_id(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.document:
            caption = f"""⬆️ Siz yuborgan qo'shimcha hujjat ⬆️
\nMurojaatingiz yuborish uchun tayyor!\n
<b>Muammo turi:</b> {data['problem_type_name']}
<b>Murojaatning to'liq shakli:</b>\n{data['user_message']}"""
            data["document_id"] = message.document.file_id
            bot.set_state(user_id, MessageStates.submit, chat_id)
            if len(caption) >= 1024:
                caption_0 = caption[:1020] + "..."
                caption_1 = caption[1020:]
                bot.send_document(
                    chat_id, 
                    document=message.document.file_id, 
                    caption=caption_0, parse_mode='html')
                bot.send_message(chat_id, caption_1, reply_markup=send_appeals_btn())
            else:
                bot.send_document(
                    chat_id, 
                    document=message.document.file_id, 
                    caption=caption, parse_mode='html', 
                    reply_markup=send_appeals_btn())



'''Rasm-ni qismi'''


@bot.message_handler(content_types=["photo"], state=MessageStates.photo_id)
def reaction_photo_id(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.photo:
            photo = message.photo[0].file_id
            caption = f"""⬆️ Siz yuborgan qo'shimcha rasm ⬆️
\nMurojaatingiz yuborish uchun tayyor!\n
<b>Muammo turi:</b> {data['problem_type_name']}
<b>Murojaatning to'liq shakli:</b>\n{data['user_message']}"""
            data["photo_id"] = photo
            bot.set_state(user_id, MessageStates.submit, chat_id)
            if len(caption) >= 1024:
                caption_0 = caption[:1020] + "..."
                caption_1 = caption[1020:]
                bot.send_photo(
                    chat_id, 
                    photo=photo, 
                    caption=caption_0,
                    parse_mode='html'
                )
                bot.send_message(chat_id, caption_1, reply_markup=send_appeals_btn())
            else:
                bot.send_photo(
                    chat_id, 
                    photo=photo, 
                    caption=caption,
                    parse_mode='html', 
                    reply_markup=send_appeals_btn())


'''Video-ni qismi'''


@bot.message_handler(content_types=["video"], state=MessageStates.video_id)
def reaction_video_id(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.video:
            video = message.video.file_id
            caption = f"""⬆️ Siz yuborgan qo'shimcha video ⬆️
\nMurojaatingiz yuborish uchun tayyor!\n
<b>Muammo turi:</b> {data['problem_type_name']}
<b>Murojaatning to'liq shakli:</b>\n{data['user_message']}"""
            data["video_id"] = video
            bot.set_state(user_id, MessageStates.submit, chat_id)
            if len(caption) >= 1024:
                caption_0 = caption[:1020] + "..."
                caption_1 = caption[1020:]
                bot.send_video(
                    chat_id, 
                    video=video,
                    caption=caption_0,
                    parse_mode='html'
                )
                bot.send_message(chat_id, caption_1, reply_markup=send_appeals_btn())
            else:
                bot.send_video(
                    chat_id, 
                    video=video,
                    caption=caption,
                    parse_mode='html', 
                    reply_markup=send_appeals_btn())



# --- User enters Ro'yxatdan otish 📄, bot asks f_name ---

@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan otish 📄")
def reaction_register(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    bot.set_state(user_id, RegisterStates.f_name, chat_id)
    bot.send_message(chat_id, "Ism, familiya va otangizning ismini kiriting", reply_markup=ReplyKeyboardRemove())


# --- The end of User enters Ro'yxatdan otish 📄, bot asks f_name ---


# # --- User enters f_name, bot asks l_name ---

@bot.message_handler(content_types=['text'], state=RegisterStates.f_name)
def reaction_f_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    f_name = message.text.strip()

    if any(char.isdigit() for char in f_name):
        bot.send_message(chat_id, "Iltimos, ismingizda raqam (son) bo'lmasin!")
        return

    with bot.retrieve_data(user_id, chat_id) as data:
        data['f_name'] = f_name

    bot.set_state(user_id, RegisterStates.gender, chat_id)
    bot.send_message(chat_id, "Jinsingizni kiriting", reply_markup=gender())


# --- The end of User enters lastname, bot asks surname ---


# --- User enters gender, bot asks birth_date ---

@bot.message_handler(content_types=['text'], state=RegisterStates.gender)
def reaction_gender(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    gender = message.text.capitalize()

    if gender not in ["Erkak", "Ayol"]:
        bot.send_message(chat_id, "Faqat 'Erkak' yoki 'Ayol' javobini yubora olasiz")
        return

    with bot.retrieve_data(user_id, chat_id) as data:
        data['gender'] = gender

    bot.set_state(user_id, RegisterStates.birth_date, chat_id)
    bot.send_message(chat_id, "Iltimos, tug'ilgan kuningizni\n"
                              "nuqta bilan ajratilgan holatda\n"
                              "quyidagi berilgan formatdagidek kiriting\n"
                              "Format: 09.11.2004", reply_markup=ReplyKeyboardRemove())

# --- The end of User enters gender, bot asks birth_date ---


# --- User enters birth_date, bot asks number ---

@bot.message_handler(content_types=['text'], state=RegisterStates.birth_date)
def reaction_birth_date(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    birth_date_parts = message.text.split('.')
    if len(birth_date_parts) != 3:
        bot.send_message(chat_id, "Iltimos, tug'ilgan kuningizni nuqta bilan ajratilgan holatda\n"
                                  "quyidagi berilgan formatdagidek kiriting (Format: 09.11.2004)")
        return

    day, month, year = birth_date_parts
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        bot.send_message(chat_id, "Iltimos, tug'ilgan kuningizni nuqta bilan ajratilgan holatda\n"
                                  "quyidagi berilgan formatdagidek kiriting (Format: 09.11.2004)")
        return

    day = int(day)
    month = int(month)
    year = int(year)

    if not (1 <= day <= 31 and 1 <= month <= 12 and year >= 1900):
        bot.send_message(chat_id, "Iltimos, kun, oy va yil-ni to'g'ri kiriting!")
        return

    current_year = datetime.now().year
    if current_year - year < 18 and year < current_year:
        bot.send_message(chat_id, "Murojaat yozish uchun yoshingiz 18 dan katta bo'lishi kerak!\n"
                                  "/start buyrug'i orqali bot-ni qayta ishga tushirishingiz mumkin\n"
                                  "Yoki tug'ilgan kuningizni qaytadan yuboring!")
        return

    elif year > current_year:
        bot.send_message(chat_id, "Iltimos, kun, oy va yil-ni to'g'ri kiriting!")
        return

    birth_date = '.'.join(birth_date_parts)
    db_birth_date = '.'.join(birth_date_parts[::-1])

    with bot.retrieve_data(user_id, chat_id) as data:
        data['birth_date'] = birth_date
        data['db_birth_date'] = db_birth_date

    contact_button = KeyboardButton("👉Raqamni yuborish👈", request_contact=True)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(contact_button)

    bot.set_state(user_id, RegisterStates.number, chat_id)
    bot.send_message(chat_id, "Pastdagi tugmani bosib, telefon raqamingizni yuboring 👇", reply_markup=share_contact())


# --- The end of User enters birth_date, bot asks number ---


# --- User enters number, bot asks city ---

@bot.message_handler(content_types=['text', 'contact'], state=RegisterStates.number)
def reaction_number(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.content_type == 'text':
        bot.send_message(chat_id, "Iltimos, pastdagi tugmani bosib, telefon raqamingizni yuboring 👇",
                         reply_markup=share_contact())
        return

    number = message.contact.phone_number

    with bot.retrieve_data(user_id, chat_id) as data:
        data['number'] = number

    bot.set_state(user_id, RegisterStates.city, chat_id)
    bot.send_message(chat_id, "Iltimos, yashash shahringizni yoki tumaningizni kiriting", reply_markup=city())


# --- The end of User enters number, bot asks city ---


# --- User enters city, bot asks street ---

@bot.message_handler(content_types=['text'], state=RegisterStates.city)
def reaction_city(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    city = message.text.capitalize()

    if city not in db.get_all_regions_name():
        bot.send_message(chat_id, "Siz kiritgan shahar yoki tuman ro'yxatda mavjud emas!\n"
                                  "Iltimos, ro'yxatda berilgan shahar yoki tumanni kiriting!")
        return

    with bot.retrieve_data(user_id, chat_id) as data:
        data['city'] = city.replace("'", "`")

    bot.set_state(user_id, RegisterStates.street, chat_id)
    bot.send_message(chat_id, "Manzilingizni yozing", reply_markup=ReplyKeyboardRemove())


# --- The end of User enters city, bot asks street ---

# --- User enters street, bot asks submit ---

@bot.message_handler(content_types=['text'], state=RegisterStates.street)
def reaction_street(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    street = message.text

    with bot.retrieve_data(user_id, chat_id) as data:
        data['street'] = street

    bot.set_state(user_id, RegisterStates.submit, chat_id)
    bot.send_message(chat_id, f"""Hamma ma'lumotlar to'g'rimi?\n
<b>Ism: {data['f_name'].title()}
Jins: {data['gender'].capitalize()}
Tug'ilgan kuni: {data['birth_date']}
Raqam: {data['number']}
Shahar yoki Tuman: {data['city'].capitalize()}
Mahalla va manzil: {data['street']}
</b>\nMa'lumotlarni saqlash uchun 'Ha' tugmasini bosing\nMa'lumotlarni qaytadan kiritish uchun 'Yo'q' tugmasini bosing""",
                     parse_mode='html', reply_markup=register_submit_btn())


# --- The end of User enters street, bot asks submit ---


@bot.message_handler(content_types=['text'], state=RegisterStates.submit)
def reaction_submit(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    submit = message.text
    if message.text == 'Ha':
        with bot.retrieve_data(user_id, chat_id) as data:
            data['telegram_id'] = user_id
            db.insert_user(**data)
        bot.send_message(chat_id, "Ro'yxatdan muvofaqqiyatli o'tdingiz!\n"
                                  "Murojaat yozish uchun /start buyrug'iga bosing", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Yo'q":
        bot.set_state(user_id, RegisterStates.f_name, chat_id)
        bot.send_message(chat_id, "Ismingizni qaytadan kiriting", reply_markup=ReplyKeyboardRemove())



