# --- Importing from other folders ---

from loader import bot, db

db.create_users_table()
db.make_appeal_type()
db.make_problem_type_table()
db.create_message_table()
db.create_regions_table()

import handlers

city_list = [
    "Bekobod shahar", "Bekobod tuman", "Bo'ka tuman", "Bo'stonliq tuman", "Chinoz tuman",
    "Chirchiq shahar", "Nurafshon shahar", "O'rtachirchiq tuman", "Ohangaron shahar", "Ohangaron tuman",
    "Olmaliq shahar", "Oqqo'rg'on tuman", "Parkent tuman", "Piskent tuman", "Qibray tuman",
    "Quyichirchiq tuman", "Toshkent tuman", "Yuqorichirchiq tuman", "Yangiyo'l shahar",
    "Yangiyo'l tuman", "Zangiota tuman", "Angren shahar"
]
appeals_type = ["Fuqoro murojaati", "Tadbirkor murojaati"]

for name in appeals_type:
    db.insert_appeals_type_table(name)

problems_type_1 = [
    "Nafaqa masalalari",
    "Bank, kredit masalalari",
    "moddy yordam masalalari",
    "Ish, ish haqi va imtiozlar",
    "Hokimiyat idoralarining ishlari",
    "Molia, soliq va bojxona masalasi",
    
]
problems_type_2 = [
    "Tashqi iqtisodiy aloqalar masalasi",
    "Davlat va hujalik idoralari ishlari",
    "Tadbirkorlikni rivojlantirish masalasi",
    "Korxona faoliati va xususiylashtirish masalasi"
]

for name in problems_type_1:
    db.insert_problem_type(1, name)

for name in problems_type_2:
    db.insert_problem_type(2, name)

for name in city_list:
    db.insert_regions_table(name.replace("'", "`"))


if __name__ == '__main__':
    print("Toshkent Hokimiga Murojaat Bot is working...")
    bot.infinity_polling()

