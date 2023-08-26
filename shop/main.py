from loader import bot, db
from parser_codes.parser_oop import UPGParser

db.create_users_table()
db.make_categories_table()
db.make_product_table()
# categories_list = ["Noutbuklar 💻", "Klaviaturalar ⌨️", "Quloqchinlar 🎧", "Sichqonchalar 🖱"]
# categories = ['kategory-mouses', 'kategory-noutbuki', 'kategory-klaviaturi', 'kategory-naushniki']

# for item in categories_list:
#     db.insert_categories_to_db(item)

# products = [UPGParser(item).get_data() for item in categories]
# for item in products:
#     for i in item:
#         db.insert_procucts(**i)


import handlers


if __name__ == "__main__":
    print("Shop is running")
    bot.polling()