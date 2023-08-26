import random
from telebot.types import (
    Message, 
    InputMediaPhoto,
    ReplyKeyboardRemove, 
)

# local variables
from config.loader import bot, db
from keyboards.inline_markup import groups_list
from keyboards.relpy_markup import (
    home_btn, categories_list, 
    example_sizes, yes_no, example_colors, old_data
)
from config.states import (ProductStates, ProductSizeState, ProductColorState)

# globals
ADMINS = db.get_admins_telegram_id()

def requared_admin(func):
    def methods(message: Message):
        if message.chat.id in ADMINS:
            func(message)
        else:
            bot.send_message(message.chat.id, "Bu ammallar faqat adminlar uchun!!!")
    return methods


@requared_admin
@bot.message_handler(regexp="Botga bog'langan Guruxlar")
def reaction_groups(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, "Barcha guruxlar", reply_markup=groups_list())


@requared_admin
@bot.message_handler(regexp="Maxsulot qo'shish")
def reaction_add_product(message: Message):
    print("start adding")
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, ProductStates.title, chat_id)
    bot.send_message(chat_id, "Maxsulotning nomini kiriting!", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"], state=ProductStates.title)
def reaction_product_title(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data["title"] = message.text.replace("'", "`")
        bot.set_state(user_id, ProductStates.description, chat_id)
        bot.send_message(chat_id, "Maxsulot xaqida ma'lumot kiriting")


@bot.message_handler(content_types=["text"], state=ProductStates.description)
def reaction_product_description(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data["description"] = message.text.replace("'", "`")
        bot.set_state(user_id, ProductStates.category_id, chat_id)
        bot.send_message(chat_id, "Maxsulotning kategoriasini tanlang", reply_markup=categories_list())


@bot.message_handler(content_types=["text"], state=ProductStates.category_id)
def reaction_product_category_id(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    categories_list = db.get_all_categories_name()
    name = message.text
    if name in categories_list:
        with bot.retrieve_data(user_id, chat_id) as data:
            data["category_id"] = db.get_category_id_by_name(name)
            data["product_pk"] = random.randint(1111111, 9999999)
            product = {
                "title": data["title"], 
                "description": data["description"], 
                "product_pk": data["product_pk"], 
                "category_id": data["category_id"], 
            }
            db.insert_products_table(**product)
            print("product_save")
            bot.set_state(user_id, ProductSizeState.size, chat_id)
            bot.send_message(chat_id, "Maxsulotni razmerini tanlang", reply_markup=example_sizes(product["product_pk"]))

    elif name not in categories_list:
        bot.set_state(user_id, ProductStates.category_id, chat_id)
        bot.send_message(chat_id, "Kechirasiz hozirda bunday kategoriya mavjud emas :(", reply_markup=categories_list())


@bot.message_handler(content_types=["text"], state=ProductSizeState.size)
def reaction_product_size(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    sizes = db.get_all_example_sizes_name()
    if message.text in sizes:
        with bot.retrieve_data(user_id, chat_id) as data:
            product_pk = data["product_pk"]
        with bot.retrieve_data(user_id, chat_id) as product_size:
            product_id = db.get_product_id_by_product_pk(int(product_pk))
            product_size["product_id"] = product_id
            product_size["size"] = message.text
            try: 
                old_price = data["price"]
                bot.set_state(user_id, ProductSizeState.price, chat_id)
                bot.send_message(chat_id, "Maxsulotning shu razmer bo'yicha narxini kiriting", reply_markup=old_data(old_price))
            except Exception as e:
                bot.set_state(user_id, ProductSizeState.price, chat_id)
                bot.send_message(chat_id, "Maxsulotning shu razmer bo'yicha narxini kiriting", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"], state=ProductSizeState.price)
def reaction_product_price(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text.isdigit():
        with bot.retrieve_data(user_id, chat_id) as product_size:
            product_size["price"] = message.text
            try:
                old_count = product_size["count"]
                bot.set_state(user_id, ProductSizeState.count, chat_id)
                bot.send_message(chat_id, "Maxsulotning shu razmer bo'yicha ombordagi qiymatini kiriting", reply_markup=old_data(old_count))
            except Exception as e:
                bot.set_state(user_id, ProductSizeState.count, chat_id)
                bot.send_message(chat_id, "Maxsulotning shu razmer bo'yicha ombordagi qiymatini kiriting", reply_markup=ReplyKeyboardRemove())

    else:
        bot.set_state(user_id, ProductSizeState.price, chat_id)
        bot.send_message(chat_id, "Maxsulot narxi faqat raqamlardan iborat bo'lishi kerak\n Iltimos qaytadan kiriting.")


@bot.message_handler(content_types=["text"], state=ProductSizeState.count)
def reaction_product_count(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text.isdigit():
        with bot.retrieve_data(user_id, chat_id) as product_size:
            product_size["count"] = message.text
            bot.set_state(user_id, ProductSizeState.save, chat_id)
            bot.send_message(chat_id, "Shu maxsulotning boshqa razmerlari ham mavjudmi ?", reply_markup=yes_no())
    else:
        bot.set_state(user_id, ProductSizeState.count, chat_id)
        bot.send_message(chat_id, "Maxsulot qiymati faqat raqamlardan iborat bo'lishi kerak\n Iltimos qaytadan kiriting.")


@bot.message_handler(content_types=["text"], state=ProductSizeState.save)
def reaction_product_size_save(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data: 
        product_pk = data["product_pk"]
        product_size = {
            "product_id": int(data["product_id"]),
            "size": data["size"],
            "price": int(data["price"]),
            "count": int(data["count"]),
        }
    if message.text == "Ha":
        db.insert_product_sizes_table(**product_size)
        bot.set_state(user_id, ProductSizeState.size, chat_id)
        bot.send_message(chat_id, "Maxsulot razmerini tanlang", reply_markup=example_sizes(product_pk))
    elif message.text == "Yoq":
        db.insert_product_sizes_table(**product_size)
        bot.set_state(user_id, ProductColorState.color, chat_id)
        bot.send_message(chat_id, "Maxsulot rangini tanlang.", reply_markup=example_colors(product_pk))
    else:
        bot.set_state(user_id, ProductSizeState.save, chat_id)
        bot.send_message(chat_id, "Iltimos 'Ha' yoki 'Yoq' tugmalaridan foydalaning.", reply_markup=yes_no())
    print("save product size")


@bot.message_handler(content_types=["text"], state=ProductColorState.color)
def reaction_product_color(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    colors = db.get_all_example_colors_name()
    if message.text in colors:
        with bot.retrieve_data(user_id, chat_id) as data:
            product_pk = data["product_pk"]
        with bot.retrieve_data(user_id, chat_id) as product_color:
            product_id = db.get_product_id_by_product_pk(int(product_pk))
            product_color["product_id"] = product_id
            product_color["color"] = message.text
            bot.set_state(user_id, ProductColorState.image, chat_id)
            bot.send_message(chat_id, "Maxsulotning shu rangidagi 1-dona rasmini yuboring", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["photo"], state=ProductColorState.image)
def reaction_product_color(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.photo:
        with bot.retrieve_data(user_id, chat_id) as product_color:
            product_color["image"] = message.photo[0].file_id
            old_price = product_color["price"]
            bot.set_state(user_id, ProductColorState.price, chat_id)
            bot.send_message(chat_id, "Maxsulotning shu rangidagi narxini", reply_markup=old_data(old_price))


@bot.message_handler(content_types=["text"], state=ProductColorState.price)
def reaction_product_color_price(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text.isdigit():
        with bot.retrieve_data(user_id, chat_id) as product_color:
            product_color["price"] = message.text
            old_count = product_color["count"]
            bot.set_state(user_id, ProductColorState.count, chat_id)
            bot.send_message(chat_id, "Maxsulotning shu rang bo'yicha ombordagi qiymatini kiriting", reply_markup=old_data(old_count))
    else:
        bot.set_state(user_id, ProductColorState.price, chat_id)
        bot.send_message(chat_id, "Maxsulot narxi faqat raqamlardan iborat bo'lishi kerak\n Iltimos qaytadan kiriting.")


@bot.message_handler(content_types=["text"], state=ProductColorState.count)
def reaction_product_color_count(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text.isdigit():
        with bot.retrieve_data(user_id, chat_id) as product_color:
            product_color["count"] = message.text
            bot.set_state(user_id, ProductColorState.save, chat_id)
            bot.send_message(chat_id, "Shu maxsulotning boshqa ranglari ham mavjudmi ?", reply_markup=yes_no())
    else:
        bot.set_state(user_id, ProductSizeState.count, chat_id)
        bot.send_message(chat_id, "Maxsulot qiymati faqat raqamlardan iborat bo'lishi kerak\n Iltimos qaytadan kiriting.")


@bot.message_handler(content_types=["text"], state=ProductColorState.save)
def reaction_product_color_save(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        product_pk = data["product_pk"]
        product_color = {
            "product_id": int(data["product_id"]),
            "color": data["color"],
            "image": data["image"],
            "price": int(data["price"]),
            "count": int(data["count"]),
        }
    if message.text == "Ha":
        db.insert_product_color_table(**product_color)
        bot.set_state(user_id, ProductColorState.color, chat_id)
        bot.send_message(chat_id, "Maxsulot rangini tanlang", reply_markup=example_colors(product_pk))
    elif message.text == "Yoq":
        db.insert_product_color_table(**product_color)
        group = db.get_all_public_groups()[0]
        bot.send_message(chat_id=group, text=f"""
            product_name: {data["title"]},
            description: {data["description"]},
        """)
        bot.send_message(chat_id, "Maxsulot saqlandi va guruxga yuborildi", reply_markup=home_btn())
        bot.delete_state(user_id, chat_id)
    else:
        bot.set_state(user_id, ProductColorState.save, chat_id)
        bot.send_message(chat_id, "Iltimos 'Ha' yoki 'Yoq' tugmalaridan foydalaning.", reply_markup=yes_no())
    print("save product color")
