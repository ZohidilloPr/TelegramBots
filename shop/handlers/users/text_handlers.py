from telebot.types import Message, ReplyKeyboardRemove

from loader import bot, db
from states import RegisterUserStates
from keyboards.inline_murkup import product_btn, products_with_pagination
from keyboards.replay_murkup import (share_contact, register_submit_btn, catgories_btn, start_btn)


@bot.message_handler(regexp="Menu 🛍")
def reaction_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Kategoriani tanlang", reply_markup=catgories_btn(db.get_all_categories()))


@bot.message_handler(regexp="Asosiy Menu  🔙")
def return_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Asosiy Menu", reply_markup=start_btn())


@bot.message_handler(func=lambda message: message.text in db.get_all_categories())
def reaction_category(message: Message):
    chat_id = message.chat.id
    category_name = message.text
    bot.send_message(chat_id, "Yuklanmoqda", reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, category_name, reply_markup=products_with_pagination(category_name))


@bot.message_handler(regexp="Ro'yhatdan o'tish ✍️")
def reaction_register(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    bot.set_state(user_id, RegisterUserStates.f_name, chat_id)
    bot.send_message(chat_id, "Ismingizni kiriting.", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"], state=RegisterUserStates.f_name)
def reaction_f_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    f_name = message.text.capitalize()
    with bot.retrieve_data(user_id, chat_id) as data:
        data["telegram_id"], data["f_name"] = user_id, f_name

    bot.set_state(user_id, RegisterUserStates.l_name, chat_id)
    bot.send_message(chat_id, "Familyangizni kiriting.")


@bot.message_handler(content_types=["text"], state=RegisterUserStates.l_name)
def reaction_l_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    l_name = message.text.capitalize()
    with bot.retrieve_data(user_id, chat_id) as data:
        data["l_name"] = l_name
        
    bot.set_state(user_id, RegisterUserStates.birth_day, chat_id)
    bot.send_message(chat_id, "Tug'ulgan sanangizni kiriting: dd.mm.yyyy")


@bot.message_handler(content_types=["text"], state=RegisterUserStates.birth_day)
def reaction_birth_date(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data["birth_day"] = ".".join(message.text.split(".")[::-1])

    bot.set_state(user_id, RegisterUserStates.phone_number, chat_id)
    bot.send_message(chat_id, "Telefon raqamizni kiriting.", reply_markup=share_contact())


@bot.message_handler(content_types=["text", "contact"], state=RegisterUserStates.phone_number)
def reaction_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.contact:
            data["phone_number"] = message.contact.phone_number
            bot.set_state(user_id, RegisterUserStates.submit, chat_id)
            bot.send_message(chat_id,
                f"""
                    <b>Ma'lumotlaringizni tekshiring!</b>
                Ism: {data["f_name"]}
                Familya: {data["l_name"]}
                Tug'ulgan sana: {data["birth_day"]}
                Telefon raqam: {data["phone_number"]}

                Barcha ma'lumotlar to'g'rimi ?
                """,
            parse_mode="html", reply_markup=register_submit_btn())
        else:
            import re
            phone = message.text
            if re.match(r"^\+?(998)?(9(0|1|3|4|5|7|8|9|)|88|33|55)\d{7}$", phone):
                data["phone_number"] = phone
                bot.set_state(user_id, RegisterUserStates.submit, chat_id)
                bot.send_message(chat_id,
                f"""
                    <b>Ma'lumotlaringizni tekshiring!</b>
                Ism: {data["f_name"]}
                Familya: {data["l_name"]}
                Tug'ulgan sana: {data["birth_day"]}
                Telefon raqam: {data["phone_number"]}

                Barcha ma'lumotlar to'g'rimi ?
                """,
                parse_mode="html", reply_markup=register_submit_btn())
            else:
                bot.set_state(user_id, RegisterUserStates.phone_number, chat_id)
                bot.send_message(chat_id, "Telefon raqamni noto'g'ri kiritdingiz iltimos qayta urunib ko'ring.", reply_markup=share_contact())



@bot.message_handler(content_types=["text"], state=RegisterUserStates.submit)
def reaction_birth_date(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        print(data)
        if message.text == "Ha":
            db.insert_users_to_db(**data)
            bot.send_message(chat_id, "Ma'lumotlar saqlandi! Botdan foydalanish uchun /start buytug'ini bosing", reply_markup=ReplyKeyboardRemove())
        elif message.text == "Yoq":
            bot.set_state(user_id, RegisterUserStates.f_name, chat_id)
            bot.send_message(chat_id, "Ma'lumotlarni boshidan kiriting.")



