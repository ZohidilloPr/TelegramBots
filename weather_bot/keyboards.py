from telebot.types import ReplyKeyboardMarkup, KeyboardButton



def start_btn():
    murkub = ReplyKeyboardMarkup(resize_keyboard=True)
    murkub.add(KeyboardButton("Ob-Havo"))
    return murkub


def RegionsBTN():
    """ tumanlar uchun replay murkub buttons """
    regions = [
        ["Andijan", "Namangan", "Fergana"],
        ["Tashkent", "Samarkand", "Bukhara"],
        ["Navoiy", "Jizzax", "Samarqand"],
        ["Qashqadaryo", "Surxondaryo", "Xorazm"],
        ["Sirdaryo", "Karakalpakstan", "Toshkent Shahri"]
    ]
    murkub = ReplyKeyboardMarkup(resize_keyboard=True) # make space for buttons
    for region_row in regions:
        murkub.row(*region_row)  # return "Andijan", "Namangan", "Fergana"
    return murkub