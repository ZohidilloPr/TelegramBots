from config.loader import bot, db


db.making_users_table() # make users table when bot start to run
db.make_groups_table() # groups table
db.make_categories_table() # product categories table
db.make_product_table() # products table
db.make_example_sizes_table() # example sizes for product_size
db.make_product_sizes_table() # product size for product
db.make_example_colors_table() # example colors for product_color
db.make_product_colors_table() # colors for product


import handlers

# installig starter data
[db.insert_categories_table(name) for name in ["Futbolkalar", "Shimlar", "Oyoq kiyimlar"]]
[db.insert_example_sizes_table(name) for name in ["S", "SL", "M", "L", "XL"]]
[db.insert_example_colors_table(name) for name in ["Oq", "Qora", "Kul Rang", "Hovo Rang", "Pushti"]]

db.set_default_admins(admins=[1789380222])



if __name__ == "__main__":
    print("Bot is running....")
    bot.polling() # for bot in developping time
    # bot.infinity_polling # for bot in running in real server
