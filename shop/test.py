from loader import db
from pprint import pprint
from parser_codes.parser_oop import UPGParser


# categories = ['kategory-mouses', 'kategory-noutbuki', 'kategory-klaviaturi', 'kategory-naushniki']
# products = [UPGParser(item).get_data() for item in categories]
# for item in products:
#     for i in item:
#         db.insert_procucts(**i)

# print(UPGParser("kategory-mouses").get_data())
# print(db.get_category_id_by_category("Noutbuklar 💻"))
# print(db.get_all_categories())

# pprint(db.filter_products_by_category_name("Noutbuklar 💻")[0])