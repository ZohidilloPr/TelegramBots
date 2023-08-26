import psycopg2


class Database:
    def __init__(self, db_name, db_password, db_host, db_user):
        self.db_connect = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )

    def maneger(self, sql, *args, fetchone:bool=False, fetchall:bool=False, commit:bool=False):
        with self.db_connect as db:
            cursor = db.cursor()
            cursor.execute(sql)

            if commit:
                return db.commit()
            elif fetchall:
                return cursor.fetchall()
            elif fetchone:
                return cursor.fetchone() 
            

    def create_users_table(self):
        """ users table create method """
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL NOT NULL PRIMARY KEY,
                telegram_id BIGINT NOT NULL UNIQUE,
                f_name VARCHAR(50),
                l_name VARCHAR(50),
                phone_number VARCHAR(15),
                birth_date DATE,
                register_time DATE DEFAULT CURRENT_TIMESTAMP
            )
        """
        return self.maneger(sql, commit=True)
    
    
    def insert_users_to_db(self, **kwargs):
        sql = """
            INSERT INTO users (telegram_id, f_name, l_name, phone_number, birth_date)
            VALUES ('%i', '%s', '%s', '%s', DATE '%s') ON CONFLICT DO NOTHING;
        """ % (kwargs["telegram_id"], kwargs["f_name"], kwargs["l_name"], kwargs["phone_number"], kwargs["birth_day"])
        self.maneger(sql, commit=True)


    def check_user_in_db(self, telegram_id):
        """ return telegram id if user registered in shop bot """
        sql = """
            SELECT telegram_id FROM users WHERE telegram_id=%i;
        """% telegram_id
        return [item[0] for item in self.maneger(sql, fetchall=True)][0] if len(self.maneger(sql, fetchall=True)) >= 1 else False
    

    def make_categories_table(self):
        """ make categories for products """
        sql = """ 
            CREATE TABLE IF NOT EXISTS categories (
                category_id BIGSERIAL PRIMARY KEY,
                category VARCHAR (50) UNIQUE
            ) 
            """
        self.maneger(sql, commit=True)


    def insert_categories_to_db(self, category):
        sql = """ 
            INSERT INTO categories (category) 
            VALUES ('%s') ON CONFLICT DO NOTHING;
            """ % category
        self.maneger(sql, commit=True)


    def get_category_id_by_category(self, category):
        """ category name orqali category_id ni olish uchun """
        sql = " SELECT category_id FROM categories WHERE category='%s'; " % category
        return self.maneger(sql, fetchone=True)[0]

    
    def get_all_categories(self):
        sql = "SELECT category FROM categories;"
        return [item[0] for item in self.maneger(sql, fetchall=True)]


    def get_category_name_by_category_id(self, category_id):
        sql = "SELECT category FROM categories WHERE category_id=%i;" % category_id
        return self.maneger(sql, fetchone=True)[0]
    

    def make_product_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS products (
                product_id BIGSERIAL PRIMARY KEY,
                product_name TEXT UNIQUE,
                link TEXT,
                image TEXT,
                price INTEGER,
                category_id INTEGER REFERENCES categories(category_id)
            );
        """    
        self.maneger(sql, commit=True)


    def insert_procucts(self, product_name, link, image, price, category_id):
        sql = """
            INSERT INTO products (product_name, link, image, price, category_id) 
            VALUES ('%s','%s', '%s', '%s', '%s') ON CONFLICT DO NOTHING;
        """ % (product_name, link, image, price, category_id)
        self.maneger(sql, commit=True)

    
    def filter_products_by_category_name(self, category_name):
        """ categoria orqali productlarni filterlash """
        # SELECT products.product_name, categories.category FROM products LEFT JOIN categories ON products.category_id=categories.category_id WHERE categories.category='Noutbuklar 💻';
        sql = """
                SELECT products.product_id, products.product_name, products.link, products.image, products.price, categories.category FROM products 
                LEFT JOIN categories ON products.category_id=categories.category_id 
                WHERE category='%s';
            """ % category_name
        return self.maneger(sql, fetchall=True)
    
    def get_products_with_pagination(self, category_name, offset, limit):
        sql = """
                SELECT products.product_id, products.product_name, products.link, products.image, products.price, categories.category FROM products 
                LEFT JOIN categories ON products.category_id=categories.category_id 
                WHERE categories.category='%s' OFFSET %s LIMIT %s;
            """ % (category_name, offset, limit)
        return self.maneger(sql, fetchall=True)
        

    def get_products_count(self, category_name):
        sql = """
                SELECT COUNT(products.product_id) FROM products 
                LEFT JOIN categories ON products.category_id=categories.category_id 
                WHERE categories.category='%s'; 
            """ % category_name
        return self.maneger(sql, fetchone=True)[0]
    

    def get_product_by_id(self, product_id):
        sql = "SELECT * FROM products WHERE product_id=%i" % product_id
        return self.maneger(sql, fetchone=True)
        
