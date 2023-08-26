from telebot.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InputFile, CallbackQuery

)

from loader import bot, db
from config import ADMINS, GROUP_CHAT_ID, RESPOND_GROUPS
from keyboards.inline import quarter_btn
from keyboards.default import (
    admin_btn,
    go_back_btn,
    hisobot_type_btn, to_excel, appeals_type, problem_type
)
from states import (
    AdminStates,
    AddProblemType,
    RemoveProblemType, SeeAllAppeals
)



def requared_admin(func):
    def methods(message: Message):
        group_admins = bot.get_chat_administrators(GROUP_CHAT_ID)
        admins = [item.user.id for item in group_admins]
        if message.from_user.id in admins:
            func(message)
        else:
            bot.send_message(message.chat.id, "Bu buyruqlar faqat adminlar uchun")

    return methods


@requared_admin
@bot.message_handler(regexp="Hisobot")
def reaction_hisobot(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Muddatni tanlang", reply_markup=hisobot_type_btn())


@requared_admin
@bot.message_handler(regexp="Haftalik")
def reaction_week(message: Message):
    chat_id = message.chat.id
    file = InputFile(db.get_in_the_week_messages())
    bot.send_document(chat_id=chat_id, document=file, caption="Haftalik murojaatlar hisoboti")


@requared_admin
@bot.message_handler(regexp="Oylik")
def reaction_month(message: Message):
    chat_id = message.chat.id
    file = InputFile(db.get_in_the_month_messages())
    bot.send_document(chat_id=chat_id, document=file, caption="Oylik murojaatlar hisoboti")


@requared_admin
@bot.message_handler(regexp="Chorak")
def reaction_quarter(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Iltimos Chorakni tanlang: ", reply_markup=quarter_btn())


@requared_admin
@bot.message_handler(regexp="Yil")
def reaction_year(message: Message):
    chat_id = message.chat.id
    file = InputFile(db.get_in_this_year_problems_report())
    bot.send_document(chat_id=chat_id, document=file, caption=f"Shu yillik umumiy murojatlari")


@requared_admin
@bot.message_handler(regexp="Foydalanuvchining barcha murojatlarni ko'rish")
def reaction_see_btn(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, SeeAllAppeals.user_id, chat_id)
    bot.send_message(chat_id, "Buning uchun userning id-sini yuboring!", reply_markup=go_back_btn())


@requared_admin
@bot.message_handler(content_types=["text"], state=SeeAllAppeals.user_id)
def reaction_give_appeals(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    id = message.text
    if id.isdigit() and '-' not in id:
        id = int(id)
        with bot.retrieve_data(user_id, chat_id) as data:
            data["id"] = id
        try:
            user = db.get_user_from_telegram_id(id)
            if user is not None:
                count_appeals = db.get_report_by_user(user[0])
                if count_appeals != []:
                    user_data = f"""Foydalanuvchi xaqida ma'lumot:
    To'liq ismi: {user[2]}
    Jinsi: {user[3]}
    Tug'ulgan sana: {user[4]}
    Telefon raqam: {user[6]}
    Manzili: {user[7]} {user[8]}
    Umumiy murojatlar soni: {count_appeals[0][1]}-ta
    """
                else:
                    user_data = f"""Foydalanuvchi xaqida ma'lumot:
    To'liq ismi: {user[2]}
    Jinsi: {user[3]}
    Tug'ulgan sana: {user[4]}
    Telefon raqam: {user[6]}
    Manzili: {user[7]} {user[8]}
    Umumiy murojatlar soni: <Murojat yubormagan>
    """
                bot.send_message(chat_id, user_data)
            check = db.check_user(id)
            if check:
                messages = db.user_message(id)
                if messages:
                    for user_message in messages:
                        problem_type = db.get_problem_type_name_by_id(id=int(user_message[0]))
                        full_message = user_message[1]
                        register_time = user_message[5]
                        register_time_formatted = register_time.strftime("%Y-%m-%d %H:%M")
                        caption = f"""⬆️ <b>Siz yuborgan qo'shimcha ma'lumot</b> ⬆️
<b>Muammo turi:</b> {problem_type}
<b>To'liq murojaat matni:</b> {full_message}
<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}"""
                        if user_message[2] != " ":  # for document_id
                            if len(caption) >= 1024:
                                caption_0 = caption[:1020] + "..."
                                caption_1 = caption[1020:]
                                bot.send_document(
                                    chat_id=chat_id,
                                    document=user_message[2],
                                    caption=caption_0,
                                    parse_mode='html'
                                )
                                bot.send_message(chat_id, caption_1, parse_mode='html')
                            else:
                                bot.send_document(
                                    chat_id=chat_id,
                                    document=user_message[2],
                                    caption=caption,
                                    parse_mode='html'
                                ) 
                        elif user_message[3] != " ":  # for photo
                            if len(caption) >= 1024:
                                caption_0 = caption[:1020] + "..."
                                caption_1 = caption[1020:]
                                bot.send_photo(
                                    chat_id=chat_id,
                                    photo=user_message[3],
                                    caption=caption_0,
                                    parse_mode='html'
                                )
                                bot.send_message(chat_id, caption_1, parse_mode='html')
                            else:
                                bot.send_photo(
                                    chat_id=chat_id,
                                    photo=user_message[3],
                                    caption=caption,
                                    parse_mode='html'
                                ) 

                        elif user_message[4] != " ":  # for video
                            if len(caption) >= 1024:
                                caption_0 = caption[:1020] + "..."
                                caption_1 = caption[1020:]
                                bot.send_video(
                                    chat_id,
                                    video=user_message[4],
                                    caption=caption_0,
                                    parse_mode='html'
                                )
                                bot.send_message(chat_id, caption_1, parse_mode='html')
                            else:
                                bot.send_video(
                                    chat_id,
                                    video=user_message[4],
                                    caption=caption,
                                    parse_mode='html'
                                )
                        else:
                            bot.send_message(chat_id,
                                             f"<b>Qo'shimcha hujjatlar:</b> Mavjud emas\n\n<b>Muammo turi:</b> {problem_type}\n\n<b>To'liq murojaat matni:</b> {full_message}\n\n<b>Murojaat yuborilgan vaqti:</b> {register_time_formatted}\n\n",
                                             parse_mode='html'),
                    bot.set_state(user_id, SeeAllAppeals.to_excel, chat_id)
                    bot.send_message(chat_id, "Barcha malumotlarni excelga yuklab olishingiz ham mumkun!",
                                     reply_markup=to_excel())
            else:
                bot.set_state(user_id, SeeAllAppeals.user_id, chat_id)
                bot.send_message(chat_id, "Bizning bazamizda bunday foydalanuvchi topilmadi!")

        except Exception as e:
            bot.set_state(user_id, SeeAllAppeals.user_id, chat_id)
            bot.send_message(chat_id, f"siz yuborgan user id bilan muommo chiqdi iltimos qaytadan yuboring\nError: {e}")
    elif id == "Orqaga qaytish":
        bot.delete_state(user_id, chat_id)
        bot.send_message(chat_id, "Bekor qilindi!", reply_markup=admin_btn())
    else:
        bot.set_state(user_id, SeeAllAppeals.user_id, chat_id)
        bot.send_message(chat_id, "User id faqat raqamlardan iborat bo'lishi kerak")


@requared_admin
@bot.message_handler(content_types=["text"], state=SeeAllAppeals.to_excel)
def reaction_back(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text == "Orqaga qaytish":
        bot.delete_state(user_id, chat_id)
        bot.send_message(chat_id, "Bekor qilindi!", reply_markup=admin_btn())
    elif text == "Ma'lumotlarni excel faylda yuklab olish":
        with bot.retrieve_data(user_id, chat_id) as data:
            id = data["id"]
        file = InputFile(db.get_all_appeals_by_user(id))
        bot.delete_state(user_id, chat_id)
        bot.send_document(chat_id, file, caption="Umumiy hisobot")
    else:
        bot.set_state(user_id, SeeAllAppeals.to_excel, chat_id)
        bot.send_message(chat_id, "Iltimos pastda ko'rsatilayotgan tugmalardan foydalaning.")


@requared_admin
@bot.message_handler(regexp="Orqaga qaytish")
def reaction_back(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Orqaga qaytdingiz", reply_markup=admin_btn())


@requared_admin
@bot.message_handler(func=lambda message: message.text == "Foydalanuvchilar soni")
def reaction_count_user(message: Message):
    chat_id = message.chat.id
    count = db.get_count_users()
    bot.send_message(chat_id, f"Foydalanuvchilar soni: {count}")


@requared_admin
@bot.message_handler(func=lambda message: message.text == "Habar yuborish")
def reaction_send_message_users(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, AdminStates.message, chat_id)
    bot.send_message(chat_id, f"Barcha foydalanuvchilarga yuborish uchun xabar kiriting:",
                     reply_markup=ReplyKeyboardRemove())


@requared_admin
@bot.message_handler(content_types=['photo', 'video', 'text', 'document'], state=AdminStates.message)
def reaction_send_message(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    users = db.get_users_id()
    for i in users:
        bot.copy_message(i, chat_id, message.id)
    bot.send_message(chat_id, "⬆️ Habar yuqorida ko'rsatilgan shaklda yuborildi! ⬆️", reply_markup=admin_btn())
    bot.delete_state(user_id, chat_id)


@requared_admin
@bot.message_handler(func=lambda message: message.text == "Muammo turini qo'shish")
def reaction_problem_add(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, AddProblemType.appeals_type, chat_id)
    bot.send_message(chat_id, "Qaysi bo'limga qo'shmoqchisiz.",
                     reply_markup=appeals_type())



@requared_admin
@bot.message_handler(content_types=["text"], state=AddProblemType.appeals_type)
def reaction_appeals_type(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text in db.get_all_appeals_type_name():
        with bot.retrieve_data(user_id, chat_id) as data:
            data["appeals_type_id"] = db.get_appeals_id_by_appeal_type_name(text)
            bot.set_state(user_id, AddProblemType.name, chat_id)
            bot.send_message(chat_id, "Qo'shish kerak bo'lgan yangi muammo turini nomini jo'nating!",
                             reply_markup=go_back_btn())


@requared_admin
@bot.message_handler(content_types=["text"], state=AddProblemType.name)
def reaction_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text != "Orqaga qaytish":
        if db.get_problem_type_id_by_name(message.text):
            bot.send_message(chat_id, f"'{message.text}' - muammo turi allaqachon mavjud!\n"
                                      f"Boshqa muammo turi nomini qo'shish uchun jo'nating yoki\n"
                                      f"'Orqaga qaytish' tugmasini orqaga qaytish uchun bosing!")

        elif db.get_problem_type_id_by_name(message.text) is None:
            with bot.retrieve_data(user_id, chat_id) as data:
                db.insert_problem_type(int(data["appeals_type_id"]), message.text)
                bot.send_message(chat_id, f"'{message.text}' - muammo turi qo'shildi!", reply_markup=admin_btn())
        bot.delete_state(user_id, chat_id)

    elif message.text == "Orqaga qaytish":
        bot.delete_state(user_id, chat_id)


@requared_admin
@bot.message_handler(regexp="Muammo turini o'chirish")
def reaction_delete_btn(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, RemoveProblemType.appeals_type, chat_id)
    bot.send_message(chat_id, "Qaysi bo'limdan o'chiramiz", reply_markup=appeals_type())


@requared_admin
@bot.message_handler(content_types=["text"], state=RemoveProblemType.appeals_type)
def reaction_appeals_type(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text in db.get_all_appeals_type_name():
        with bot.retrieve_data(user_id, chat_id) as data:
            data["appeals_type"] = text
            markup = problem_type(text).add(KeyboardButton("Orqaga qaytish"))
            bot.set_state(user_id, RemoveProblemType.name, chat_id)
            bot.send_message(
                chat_id, 
                "O'chirish kerak bo'lgan muommo turini tanlang", 
                reply_markup=markup
            )
    else:
        bot.set_state(user_id, RemoveProblemType.appeals_type, chat_id)
        bot.send_message(chat_id, "Iltimos faqat pastdagi tugmalardan foydalaning!", reply_markup=appeals_type())


@requared_admin
@bot.message_handler(content_types=["text"], state=RemoveProblemType.name)
def reaction_select_type(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if text in db.get_all_problem_types():
        with bot.retrieve_data(user_id, chat_id) as data:
            appeals_type = data["appeals_type"]
            id = db.get_problem_type_id_by_name(text)
            print(id)
            db.delete_problem_type(id)
            markup = problem_type(appeals_type).add(KeyboardButton("Orqaga qaytish"))
            bot.send_message(chat_id, f"{text} - o'chirildi !", reply_markup=markup)
        bot.delete_state(user_id, chat_id)
    elif text == "Orqaga qaytish":
        bot.send_message(chat_id, "Bekor qilindi", reply_markup=admin_btn())
        bot.delete_state(user_id, chat_id)


''' Javob berish part of code '''


@bot.message_handler(content_types=["text"], chat_id=RESPOND_GROUPS)
def reaction_group_chat(message: Message):
    if message.reply_to_message:
        reply_text = f"<b>Murojaatingizga javob</b>: {message.text}"
        try:
            if message.reply_to_message.text:
                sended_user = int(message.reply_to_message.text.split("|")[1])
            else:
                sended_user = int(message.reply_to_message.caption.split("|")[1])
            bot.send_message(chat_id=sended_user, text=reply_text, parse_mode="HTML")
        except Exception as e:
            print(e)




''' Javob berish part of code '''
