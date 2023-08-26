from telebot.types import CallbackQuery

from loader import bot, db
from states import CardState
from keyboards.replay_murkup import start_btn, catgories_btn
from keyboards.inline_murkup import (products_with_pagination, back_to_product_btn, product_items_in_card)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_home")
def reaction_manu_back(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Asosiy Menu", reply_markup=start_btn())


@bot.callback_query_handler(func=lambda call: call.data == "back_to_category")
def reaction_categories_back(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Kategoriani tanlang", reply_markup=catgories_btn(db.get_all_categories()))


@bot.callback_query_handler(func=lambda call: call.data == "next")
def reaction_next_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for item in keyboards_list:
        if "page" in item.callback_data:
            page = int(item.text)
            category_name = item.callback_data.split("|")[1]
            page += 1
            bot.edit_message_reply_markup(
                chat_id, call.message.id,
                reply_markup=products_with_pagination(category_name, page)
            )


@bot.callback_query_handler(func=lambda call: call.data == "preview")
def reaction_preview_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for item in keyboards_list:
        if "page" in item.callback_data:
            page = int(item.text)
            category_name = item.callback_data.split("|")[1]
            page -= 1
            bot.edit_message_reply_markup(
                chat_id, call.message.id,
                reply_markup=products_with_pagination(category_name, page)
            )
 

@bot.callback_query_handler(func=lambda call: "page" in call.data)
def reaction_page_btn(call: CallbackQuery):
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for item in keyboards_list:
        if "page" in item.callback_data:
            page = int(item.text)
            bot.answer_callback_query(call.id, f"Siz {page}-sahifadasiz!", show_alert=True)


@bot.callback_query_handler(func=lambda call: "product" in call.data)
def reaction_products_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = int(call.data.split("|")[1])
    product = db.get_product_by_id(product_id)
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for item in keyboards_list:
        if "page" in item.callback_data:
            page = int(item.text)
    product_name, link, image, price, category_id = product[1:]
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_photo(
            chat_id, image, 
            f""" 
                ✍️<b>{product_name}</b>
💰Narxi: {price}
<a href='{link}' >🔗Batafsil</a>
            """, parse_mode="HTML", reply_markup=back_to_product_btn(product_id, category_id, page))


@bot.callback_query_handler(func=lambda call: call.data == "plus")
def reaction_plus_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    quantity += 1
    category_id = int(call.message.reply_markup.keyboard[-1][0].callback_data.split("|")[1])
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split("|")[1])
    product_id = int(call.message.reply_markup.keyboard[1][0].callback_data.split("|")[1])
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=back_to_product_btn(product_id, category_id, page, quantity))


@bot.callback_query_handler(func=lambda call: call.data == "minus")
def reaction_minus_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    if quantity != 1:
        quantity -= 1
        category_id = int(call.message.reply_markup.keyboard[-1][0].callback_data.split("|")[1])
        page = int(call.message.reply_markup.keyboard[0][1].callback_data.split("|")[1])
        product_id = int(call.message.reply_markup.keyboard[1][0].callback_data.split("|")[1])
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=back_to_product_btn(product_id, category_id, page, quantity))
    else:
        bot.answer_callback_query(call.id, "Maxsulotni kamida 1-dona so'tib olsa bo'ladi", show_alert=True)


@bot.callback_query_handler(func=lambda call: "back_to_category_id" in call.data)
def reaction_back(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split("|")[1])
    category_name = db.get_category_name_by_category_id(int(call.message.reply_markup.keyboard[-1][0].callback_data.split("|")[1]))
    bot.send_message(chat_id, "Yuklanmoqda", reply_markup=products_with_pagination(category_name, page))


@bot.callback_query_handler(func=lambda call: "add_card" in call.data)
def reaction_card_add(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.set_state(user_id, CardState.card, chat_id)
    product_id = int(call.data.split("|")[1])
    product = db.get_product_by_id(product_id)
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    product_name, price = product[1], product[4]
    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get("card"):
            data["card"][product_name] = {
                "product_id": product_id,
                "quantity": quantity,
                "price": price,
            }
        else:
            data["card"] = {
                product_name:{
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": price,
                }
            }
    print(data, "add_card")
  
    
@bot.callback_query_handler(func=lambda call: "show_card" == call.data)
def reaction_card_show(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        result = get_text_murkup(data)
        text = result["text"]
        murkup = result["murkup"]
    bot.delete_message(chat_id, call.message.message_id) 
    bot.send_message(chat_id, text, reply_markup=murkup)


@bot.callback_query_handler(func=lambda call: "remove" in call.data)
def reaction_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    product_id = int(call.data.split("|")[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [product_name for product_name in data["card"].keys()]
        for item in keys:
            if data["card"][item]["product_id"] == product_id:
                del data["card"][item]

    result = get_text_murkup(data)
    text = result["text"]
    murkup = result["murkup"]
    bot.delete_message(chat_id, call.message.message_id) 
    bot.send_message(chat_id, text, reply_markup=murkup)


def get_text_murkup(data: dict):
    text = "Savat \n"
    total_price = 0
    for product, items in data["card"].items():
        product_price = items["price"]
        product_quantity = items["quantity"]
        price = int(product_price) * int(product_quantity)
        total_price += price
        text += f"""{product}
Narxi: {product_quantity} ✖️ {product_price} = {price}
"""
    if total_price == 0:
        text = "Savat bo'sh !"
        murkup = start_btn()

    else: 
        text += f"Umumiy Narx: {total_price}"
        murkup = product_items_in_card(data)
    return {
        "murkup": murkup,
        "text": text
    }


@bot.callback_query_handler(func=lambda call: call.data == "clear_card")
def reaction_clear(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)  
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Savatcha bo'shatildi", reply_markup=start_btn())
    