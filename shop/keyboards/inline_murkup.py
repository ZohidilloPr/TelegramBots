from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db



def help_btn():
    murkup = InlineKeyboardMarkup()
    murkup.add(InlineKeyboardButton("Dasturchiga yozish", url="https://t.me/zohidilloturgunov"))
    return murkup


def product_btn(products_list: list):
    murkup = InlineKeyboardMarkup()
    for product in products_list:
        murkup.add(InlineKeyboardButton(product[1], callback_data=f"product|{product[0]}"))
    return murkup


def products_with_pagination(category_name, page=1):
    murkup = InlineKeyboardMarkup()
    limit = 5
    count_products = db.get_products_count(category_name)
    max_pages = count_products // limit if count_products % limit == 0 else (count_products // limit) + 1
    offset = (page - 1) * limit
    products = db.get_products_with_pagination(category_name, offset, limit)
    for product in products:
        murkup.add(InlineKeyboardButton(product[1], callback_data=f"product|{product[0]}"))
    preview = InlineKeyboardButton("◀️", callback_data="preview")
    page_btn = InlineKeyboardButton(page, callback_data=f"page|{category_name}")
    next = InlineKeyboardButton("▶️", callback_data="next")
    if page == 1:
        murkup.row(page_btn, next)
    elif 1 < page < max_pages:
        murkup.row(preview, page_btn, next)
    elif max_pages == page:
        murkup.row(preview, page_btn)
    back_category = InlineKeyboardButton("Kategorialar", callback_data="back_to_category")
    main_menu = InlineKeyboardButton("Asosiy Menu", callback_data="back_to_home")
    murkup.row(back_category, main_menu)
    return murkup


def back_to_product_btn(product_id, category_id, page, quantity=1):
    items = [
        InlineKeyboardButton("➖", callback_data="minus"),
        InlineKeyboardButton(quantity, callback_data=f"quantity|{page}"),
        InlineKeyboardButton("➕", callback_data=f"plus"),
    ]
    cards = [
        InlineKeyboardButton("Savatga qo'shish", callback_data=f"add_card|{product_id}"),
        InlineKeyboardButton("Savat", callback_data=f"show_card"),
    ]
    menu = [
        InlineKeyboardButton("Ortga 🔙", callback_data=f"back_to_category_id|{category_id}"),
        InlineKeyboardButton("Asosiy Menu", callback_data=f"back_to_home")
    ]
    return InlineKeyboardMarkup(keyboard=[items, cards, menu])


def product_items_in_card(data: dict):
    murkup = InlineKeyboardMarkup(row_width=1)
    for product, items in data["card"].items():
        product_id = items["product_id"]
        murkup.add(InlineKeyboardButton(f"❌ {product}", callback_data=f"remove|{product_id}"))
    back = InlineKeyboardButton("Ortga 🔙", callback_data=f"back_to_category_id")
    clear = InlineKeyboardButton("Tozalash 🧹", callback_data="clear_card")
    order = InlineKeyboardButton("Tasdiqlash ✅", callback_data="order")
    murkup.row(back, order)
    murkup.add(clear)
    return murkup