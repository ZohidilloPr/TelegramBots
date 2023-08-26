# --- Importing from libraries ---
import os
import random
import psycopg2
import datetime
import pandas as pd
from pathlib import Path
from decouple import config
from sqlalchemy import create_engine

# --- The end of Importing from libraries ---


# --- Creating DataBase class ---

class DataBase:
    __media_folder = Path(f"{os.getcwd()}/media").mkdir(parents=True, exist_ok=True)
    def __init__(self, db_name, db_password, db_host, db_user):
        self.db_connect = psycopg2.connect(
            database=db_name,
            host=db_host,
            user=db_user,
            password=db_password,
        )
        self.media = f"{os.getcwd()}/media/"
    # --- Creating manager function ---

    def manager(self, sql, *args, fetchone: bool = False, fetchall: bool = False, commit: bool = False):
        with self.db_connect as db:
            cursor = db.cursor()
            cursor.execute(sql, args)

            if commit:
                return db.commit()
            elif fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()

    # --- The end of Creating manager function ---

    # --- Creating of DataBase of users named  create_users_table ---

    def create_users_table(self):
        sql = """CREATE TABLE IF NOT EXISTS users(
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT,
            f_name VARCHAR(100),
            gender VARCHAR(20),
            birth_date VARCHAR(20),  
            db_birth_date DATE,     
            number VARCHAR(20),
            city VARCHAR(50),
            street VARCHAR(100),
            add_date DATE DEFAULT current_timestamp      
        )"""
        return self.manager(sql, commit=True)

    # --- The end of Creating of DataBase of users named  create_users_table ---


    # --- Creating of DataBase of users named  create_problems_table ---

    def create_problems_table(self):
        sql = """CREATE TABLE IF NOT EXISTS problems(
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) NOT NULL, 
            user_problem_type VARCHAR(50),
            user_message VARCHAR(15000), 
            add_date DATE DEFAULT current_timestamp       
        )"""
        return self.manager(sql, commit=True)

    # --- The end of Creating of DataBase of users named  create_problems_table ---


    def get_user_id_from_telegram_id(self, user_id):
        sql = """ SELECT id FROM users WHERE telegram_id='%i' """ % user_id
        return self.manager(sql, fetchone=True)[0]

    def get_user_from_telegram_id(self, user_id):
        sql = """ SELECT * FROM users WHERE telegram_id='%i' """ % user_id
        return self.manager(sql, fetchone=True)
    # --- Checking uniqueness of user ---

    def check_user(self, telegram_id):
        sql = """SELECT telegram_id FROM users WHERE telegram_id='%i'""" % telegram_id
        return True if self.manager(sql, fetchone=True) else False
    

    def get_report_by_user(self, user_id):
        """ 
            user id orqali murojatlar hisobotini olish uchun
            masalan: necha bora murojat yuborgan
            return data: [('Bo`stonliq tumani', 13, 0, 0, 2, 11)]
        """
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
               for a_type in self.get_all_appeals_type_name()
            ]
        )
        sql = f"""
            SELECT
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city,
                users.id
            HAVING 
                users.id={user_id}
            ORDER BY
                users.city;
        """
        return self.manager(sql, fetchall=True)



    def insert_user(self, telegram_id, f_name, gender, birth_date, db_birth_date, number, city, street):
        telegram_id = int(telegram_id)
        sql = """INSERT INTO users (telegram_id, f_name, gender, birth_date, db_birth_date, number, city, street) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        return self.manager(sql, telegram_id, f_name, gender, birth_date, db_birth_date, number, city, street,
                            commit=True)

    # --- The end of Saving a new user function ---

    def make_appeal_type(self):
        sql = """
            CREATE TABLE IF NOT EXISTS appeals_type(
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR (50) UNIQUE,
                register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.manager(sql, commit=True)
    

    def insert_appeals_type_table(self, name):
        sql = """
            INSERT INTO appeals_type (name)
            VALUES ('%s') ON CONFLICT DO NOTHING;
        """ % name
        self.manager(sql, commit=True)

    
    def get_appeals_id_by_appeal_type_name(self, name):
        sql = "SELECT id FROM appeals_type WHERE name='%s';" % name
        return self.manager(sql, fetchone=True)[0]


    def get_all_appeals_type_name(self):
        sql = "SELECT name FROM appeals_type;"
        return [item[0] for item in self.manager(sql, fetchall=True)]
    
    def get_all_appeals_type(self):
        sql = "SELECT id, name FROM appeals_type;"
        return self.manager(sql, fetchall=True)

    def update_appeals_type_name(self, id, new_name):
        sql = "UPDATE appeals_type SET name = '%s' WHERE id = '%i';" % (new_name, id)
        self.manager(sql, commit=True)


    def create_message_table(self):
        sql = """CREATE TABLE IF NOT EXISTS problems(
            id BIGSERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            appeals_type_id INTEGER REFERENCES appeals_type(id),
            problem_type_id INTEGER REFERENCES problem_type(id),
            user_message TEXT NOT NULL,
            document_id TEXT,
            photo_id TEXT,
            video_id TEXT,
            register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """
        self.manager(sql, commit=True)


    def insert_messages_table(self, user, appeals_type_id, problem_type, user_message, document_id, photo_id, video_id):
        sql = """
            INSERT INTO problems (user_id, appeals_type_id, problem_type_id, user_message, document_id, photo_id, video_id)
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
        """ % (user, appeals_type_id, problem_type, user_message, document_id, photo_id, video_id)
        self.manager(sql, commit=True)


    def set_media_folder_name(self):
        """ folder name set """
        current_time = datetime.datetime.now()
        current_hour = f"{current_time.hour}_{current_time.minute}"
        week_days = {
            0: "Dushanba",
            1: "Seshanba",
            2: "Chorshanba",
            3: "Payshanba",
            4: "Juma",
            5: "Shanba",
            6: "Yakshanba",
        }
        media_folder_name = f"{self.media}{current_time.date()}/{week_days[current_time.weekday()]}/{current_hour}/"
        os.makedirs(media_folder_name, exist_ok=True)
        return media_folder_name
    
    def save_dataframes_to_excel(self, sql, sql_1, sql_2, file_name):
        """ generate excel file and return file path """
        engine_psql = create_engine(config("POSTGRES_ENGINE"))
        dataframe = pd.read_sql_query(sql, engine_psql)
        dataframe_1 = pd.read_sql_query(sql_1, engine_psql)
        dataframe_2 = pd.read_sql_query(sql_2, engine_psql)

        if os.path.exists(f"{self.set_media_folder_name()}/{file_name}.xlsx"):
            file_path = f"{self.set_media_folder_name()}/{file_name}_request={random.randint(1111, 9999)}.xlsx"
        else:
            file_path = f"{self.set_media_folder_name()}/{file_name}.xlsx"
        
        with pd.ExcelWriter(file_path, engine="openpyxl") as data:
            dataframe_1.to_excel(data, sheet_name="Hisobot", index=False, engine="openpyxl")
            dataframe_2.to_excel(data, sheet_name="Hisobot 2", index=False, engine="openpyxl")
            dataframe.to_excel(data, sheet_name="Barcha murojaatlar", index=False, engine="openpyxl")
            for sq_2 in self.get_all_appeals_type_name():
                sql__3 = sql + "AND appeals_type.name='%s' ORDER BY problems.register_time;" % sq_2
                dataf_3 = pd.read_sql(sql__3, engine_psql)   
                dataf_3.to_excel(data, sheet_name=sq_2, index=False, engine="openpyxl") 
            # for name in self.get_all_problem_types():
            #     sql__1 = sql + "AND problem_type.name='%s' ORDER BY problems.register_time;" % name
            #     dataf = pd.read_sql(sql__1, engine_psql)   
            #     dataf.to_excel(data, sheet_name=name, index=False, engine="openpyxl")
            for sq in self.get_all_regions_name():
                sql__2 = sql + "AND users.city='%s' ORDER BY problems.register_time;" % sq
                dataf_2 = pd.read_sql(sql__2, engine_psql)   
                dataf_2.to_excel(data, sheet_name=sq, index=False, engine="openpyxl") 

        engine_psql.dispose()
        return file_path
        

    def get_all_appeals_by_user(self, telegram_id):
        """ userning barcha murojatlari """
        user_id = self.get_user_from_telegram_id(telegram_id)
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
        sql = """
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
                users.id=%i
            
        """ % user_id[0]

        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city,
                users.id
            HAVING 
                users.id={user_id[0]}
            ORDER BY
                users.city;
        """
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                problem_type.name,
                users.id
            HAVING 
                users.id={user_id[0]}
            ORDER BY
                problem_type.name;
        """
        file_name = f"{user_id[2]}_ning_barcha_murjojaatlari"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)
        

    def get_in_the_week_messages(self):
        """ haftalik murojatlar jadvali """
        current_date = datetime.datetime.now()
        current_week = current_date.isocalendar()[1]
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
        sql = """
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
                DATE_PART('week', DATE(problems.register_time))=%i
            
        """ % current_week

        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city,
                DATE_PART('week', DATE(problems.register_time))
            HAVING 
                DATE_PART('week', DATE(problems.register_time))={current_week}
            ORDER BY
                users.city;
        """
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                problem_type.name,
                DATE_PART('week', DATE(problems.register_time))
            HAVING 
                DATE_PART('week', DATE(problems.register_time))={current_week}
            ORDER BY
                problem_type.name;
        """
        file_name = f"shu_haftadagi_murojatlar_hisoboti"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)


    def get_in_the_month_messages(self):
        """ oylik murojatlar jadvali """
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
        sql = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY problems.register_time) AS "T/r",
                users.f_name AS "To'liq ismi",
                users.gender AS "Jinsi",
                users.birth_date AS "Tug'ilgan kuni",
                users.number AS "Telefon raqami",
                users.city AS "Tumani/Shahar:",
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
                DATE_PART('year', DATE(problems.register_time))=%i
            AND 
                DATE_PART('month', DATE(problems.register_time))=%i
            
        """ % (current_year, current_month)
        
        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city,
                DATE_PART('year', DATE(problems.register_time)),
                DATE_PART('month', DATE(problems.register_time))
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            AND 
                DATE_PART('month', DATE(problems.register_time))={current_month}
            ORDER BY
                users.city;
        """
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                problem_type.name,
                DATE_PART('year', DATE(problems.register_time)),
                DATE_PART('month', DATE(problems.register_time))
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            AND 
                DATE_PART('month', DATE(problems.register_time))={current_month}
            ORDER BY
                problem_type.name;
        """
        file_name = f"{current_year}-yilning_{current_month}-oyi_boyicha_murojatlar_hisoboti"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)
    

    def get_in_this_year_problems_report(self):
        current_date = datetime.datetime.now()
        current_year = current_date.year
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
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
            
        """
        
        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city,
                DATE_PART('year', DATE(problems.register_time))
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            ORDER BY
                users.city;
        """
        
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                problem_type.name,
                DATE_PART('year', DATE(problems.register_time))
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            ORDER BY
                problem_type.name;
        """

        file_name = f"{current_year}-yilning_murojatlar_hisoboti"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)


    def get_quarterly_messages(self, quarter:int):
        """ choraklik malumotlarnini olish uchun """
        current_date = datetime.datetime.now()
        current_year = current_date.year
        problem_types = self.get_all_problem_types()
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
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

        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
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
            GROUP BY 
                users.city
            ORDER BY
                users.city
        """
        
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
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
            GROUP BY 
                problem_type.name
            ORDER BY
                problem_type.name;
        """
        file_name = f"{quarter}-Chorak_murojaatlari"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)
    

    def export_messages_to_excel(self, quarter):
        """ TEST  """
        current_date = datetime.datetime.now()
        current_year = current_date.year
        problem_types = self.get_all_problem_types()
        
        problems_type_in_sql = ", \n".join(
            [
                f"COUNT(CASE WHEN problem_type.name = '{ptype}' THEN 1 ELSE NULL END) as \"{ptype} murojatlari\"" 
                for ptype in problem_types
            ]
        )
        appeals_type = ", \n".join(
            [
               f"COUNT(CASE WHEN appeals_type.name = '{a_type}' THEN 1 ELSE NULL END) as \"{a_type}\"" 
                for a_type in self.get_all_appeals_type_name()
            ]
        )
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
        sql_2 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY users.city) AS "T/r",
                users.city AS "Hududlar",
                COUNT(*) as "Jami murojatlar soni",
                {problems_type_in_sql},
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                users.city
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            AND
                DATE_PART('quarter', DATE(problems.register_time))={quarter}
            ORDER BY
                users.city
        """
        sql_1 = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY problem_type.name) AS "T/r",
                problem_type.name AS "Murojaat Turlari",
                COUNT(*) as "Jami murojatlar soni",
                {appeals_type}
            FROM problems 
                LEFT JOIN 
                    users ON users.id=problems.user_id
                LEFT JOIN 
                    problem_type ON problem_type.id = problems.problem_type_id
                LEFT JOIN 
                    appeals_type ON appeals_type.id = problems.appeals_type_id
            GROUP BY 
                problem_type.name
            HAVING 
                DATE_PART('year', DATE(problems.register_time))={current_year}
            AND
                DATE_PART('quarter', DATE(problems.register_time))={quarter}
            ORDER BY
                problem_type.name;
        """
        file_name = f"{quarter}-Chorak_murojaatlari"
        return self.save_dataframes_to_excel(sql, sql_1, sql_2, file_name)
                 

    def make_problem_type_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS problem_type(
                id BIGSERIAL PRIMARY KEY,
                appeals_type_id INTEGER REFERENCES appeals_type(id),
                name VARCHAR (50) UNIQUE NOT NULL,
                register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP               
            );
        """
        self.manager(sql, commit=True)


    def get_all_problem_types(self):
        sql = "SELECT name FROM problem_type;"
        return [item[0] for item in self.manager(sql, fetchall=True)]
    

    def get_problem_types_by_appeals_type(self, apeals_type_name):
        sql = """
            SELECT 
                problem_type.name 
            FROM 
                problem_type 
            LEFT JOIN 
                appeals_type ON appeals_type.id = problem_type.appeals_type_id 
            WHERE 
                appeals_type.name = '%s';
        """ % apeals_type_name
        return [item[0] for item in self.manager(sql, fetchall=True)]

    def insert_problem_type(self, appeals_type_id, name):
        sql = """
            INSERT INTO problem_type (appeals_type_id, name)
            VALUES ('%i', '%s') ON CONFLICT DO NOTHING;
        """ % (appeals_type_id, name)
        self.manager(sql, commit=True)

    def get_problem_type_id_by_name(self, name):
        sql = "SELECT id FROM problem_type WHERE name=%s;"
        result = self.manager(sql, name, fetchone=True)
        return result[0] if result else None


    def get_problem_type_name_by_id(self, id: int):
        sql = "SELECT name FROM problem_type WHERE id=%i;" % id
        return self.manager(sql, fetchone=True)[0]
    

    def user_message(self, telegram_id):
        user_id = self.get_user_id_from_telegram_id(telegram_id)
        if user_id:
            sql = """
                SELECT problem_type_id, user_message, document_id, photo_id, video_id, register_time FROM problems
                WHERE user_id=%s;
            """
            return [item for item in self.manager(sql, user_id, fetchall=True)]
        else:
            return []

    def get_count_users(self):
        sql = """SELECT count(telegram_id) FROM users"""
        return self.manager(sql, fetchone=True)[0]

    def get_users_id(self):
        sql = """SELECT telegram_id FROM users"""
        return [item[0] for item in self.manager(sql, fetchall=True)]

    def delete_problem_type(self, problem_type_id):
        sql = "DELETE FROM problem_type WHERE id=%s;"
        return self.manager(sql, problem_type_id, commit=True)
    

    def create_regions_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS hududlar(
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR (50) UNIQUE, 
                add_time DATE DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.manager(sql, commit=True)

    def insert_regions_table(self, name):
        sql = """
            INSERT INTO hududlar(name)
            VALUES ('%s') ON CONFLICT (name) DO NOTHING;
        """ % name
        self.manager(sql, commit=True)
    
    def get_all_regions_name(self):
        sql = """
            SELECT name FROM hududlar ORDER BY name;
        """
        return [item[0] for item in self.manager(sql, fetchall=True)]