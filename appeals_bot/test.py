# --- Little experiment that shows that our check_user function working by checking an argument ---
# --- from database a
# and show False if there is no such user in the database with this telegram_id ---
import re
import os
import datetime
from loader import db
from pathlib import Path
from pprint import pprint
from config import *

# ------------------------------------------------

# print(db.insert_problem_type('kamunal xizmatlar'))
# print(db.get_all_problem_types())

# for i in db.user_message(telegram_id=1789380222):
#     print(db.get_problem_type_name_by_id(int(i[1])))
#     if i[2] != " ":
#         print(i)
#         print()


# db.get_in_the_week_messages()
# db.get_in_the_year_messages_in_numbers()
# print(datetime.datetime.now().time().hour, datetime.datetime.now().time().minute)

# db.export_messages_to_excel("output_data.xlsx")
# current_date = datetime.datetime.now()
# current_year = current_date.year
# print("current_week: ", current_date.month)
# os.system(f"mkdir {os.getcwd()}/media")
# print(os.getcwd())
#
# print(db.get_all_regions_name())
#
# db.export_messages_to_excel(1)

# ------------------------------------------------


# --- Appeals type part ---

# for i in ["Fuqoro murojati", "Tadbirkor murojati"]:
#     db.insert_appeals_type_table(name=i)
# for i in db.get_all_appeals_type_name():
#     if re.search("tadbirkor", i):
#         print(i)

# for i in GROUPS:
#     print(GROUPS.get("fuqoro"))

# # print(db.get_report_by_user(2))
# for i in db.get_all_appeals_type():
#     print(i)

# --- The end of Appeals type part ---
current_date = datetime.datetime.now()
current_year = current_date.year
quarter = 1
sql = f"""
    SELECT 
        ROW_NUMBER() OVER (ORDER BY problems.register_time) AS "T/r",
        users.f_name AS "To'liq ismi",
        users.gender AS "Jinsi",
        users.birth_date AS "Tug'ilgan kuni",
        users.number AS "Telefon raqami",
        users.city AS "Tumani/Shahari:",
        users.street AS "Mahalla va manzili",
        appeals_type.name AS "Qanday murojaat",
        problem_type.name AS "Muammo turi",
        problems.user_message AS "Murojaatning to'liq shakli",
        problems.register_time AS "Jo'natilgan vaqti" 
    FROM problems 
        LEFT JOIN 
            users ON users.id=problems.user_id
        LEFT JOIN 
            problem_type ON problem_type.id = problems.problem_type_id
        LEFT JOIN
            appeals_type ON appeals_type.id = problems.appeals_type_id
    WHERE 
        DATE_PART('year', DATE(problems.register_time))={current_year}
    AND 
        DATE_PART('quarter', DATE(problems.register_time))={quarter}
"""
# print(sql)
# db.get_quarterly_messages(3)
# print(db.get_user_from_telegram_id(1234584556))
db.export_messages_to_excel(quarter=3)