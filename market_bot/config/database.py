import psycopg2

class Database:
    def __init__(self, db_name, db_user, db_pass, db_host):
        self.connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_pass,
            host=db_host
        )


    def maneger(self, sql, commit: bool=False, fetchall: bool=False, fetchone: bool=False):
        with self.connection as db:
            cursor = db.cursor()
            cursor.execute(sql)
            if commit:
               return db.commit()
            elif fetchall:
                return cursor.fetchall()
            elif fetchone:
                return cursor.fetchone()
    
    # making tables
    def making_users_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                telegram_id BIGSERIAL PRIMARY KEY,
                f_name VARCHAR (50),
                l_name VARCHAR (100),
                username VARCHAR (50),
                is_admin BOOLEAN DEFAULT FALSE,
                register_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            ) 
        """
        self.maneger(sql, commit=True)
    

    def insert_users_table(self, telegram_id, f_name, l_name, username):
        sql = """
            INSERT INTO users (telegram_id, f_name, l_name, username)
            VALUES ('%i', '%s', '%s', '%s') ON CONFLICT DO NOTHING
        """ % (telegram_id, f_name, l_name, username)
        self.maneger(sql, commit=True)


    def set_admins(self, admin_id: int):
        sql = "UPDATE users SET is_admin=TRUE WHERE telegram_id='%i'" % admin_id
        self.maneger(sql, commit=True)

    
    def set_default_admins(self, admins: list):
        for user in admins:
            sql = f"UPDATE users SET is_admin=TRUE WHERE telegram_id={user};"
            self.maneger(sql, commit=True)


    def get_user_from_users(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id=%i" % telegram_id
        return self.maneger(sql, fetchone=True)
    

    def get_admins_telegram_id(self):
        sql = """ SELECT telegram_id FROM users WHERE is_admin=TRUE; """
        return [int(admin[0]) for admin in self.maneger(sql, fetchall=True)]
    
    
    def check_user_exists(self, telegram_id):
        sql = """ SELECT * FROM users WHERE telegram_id=%i; """ % telegram_id
        return True if self.maneger(sql, fetchone=True) is not None else False
    

    def make_groups_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS groups(
                id BIGSERIAL PRIMARY KEY,
                chat_id VARCHAR (100) UNIQUE,
                user_name VARCHAR (100) UNIQUE,
                public BOOL DEFAULT FALSE,
                add_time DATE DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.maneger(sql, commit=True)


    def insert_group_table(self, chat_id, user_name, public=False):
        sql = """
            INSERT INTO groups (chat_id, user_name, public)
            VALUES ('%s', '%s', '%s') ON CONFLICT DO NOTHING;
        """ % (chat_id, user_name, public)
        self.maneger(sql, commit=True)


    def get_all_groups(self):
        sql = "SELECT * FROM groups;"
        return [item for item in self.maneger(sql, fetchall=True)]
    

    def set_public_group(self, chat_id):
        sql = "UPDATE groups SET public=TRUE WHERE chat_id='%s'" % chat_id
        self.maneger(sql, commit=True)


    def get_all_public_groups(self):
        sql = "SELECT chat_id FROM groups WHERE public=TRUE;"
        return [item[0] for item in self.maneger(sql, fetchall=True)]


    def make_categories_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS categories(
                id BIGSERIAL PRIMARY KEY,
                name TEXT UNIQUE,
                add_time DATE DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.maneger(sql, commit=True)


    def insert_categories_table(self, name):
        sql = """
            INSERT INTO categories (name)
            VALUES ('%s') ON CONFLICT DO NOTHING
        """ % name
        self.maneger(sql, commit=True)


    def get_all_categories_name(self):
        """ barcha maxsulot kategorialarini nomini olish uchun """
        sql = "SELECT name FROM categories"
        return [item[0] for item in self.maneger(sql, fetchall=True)]
    

    def get_category_id_by_name(self, name):
        sql = "SELECT id FROM categories WHERE name='%s'" % name
        return self.maneger(sql, fetchone=True)[0]


    def make_product_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS products(
                id BIGSERIAL PRIMARY KEY,
                title TEXT,
                description TEXT,
                product_pk INTEGER UNIQUE,
                category_id INTEGER REFERENCES categories(id),
                register_date DATE DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.maneger(sql, commit=True)


    def insert_products_table(self, title, description, product_pk, category_id):
        sql = """
            INSERT INTO products (title, description, product_pk, category_id)
            VALUES ('%s', '%s', '%i', '%i') ON CONFLICT DO NOTHING;
        """ % (title, description, product_pk, category_id)
        self.maneger(sql, commit=True)


    def get_product_id_by_product_pk(self, product_pk: int):
        sql = "SELECT id FROM products WHERE product_pk='%i'" % product_pk
        return int(self.maneger(sql, fetchone=True)[0]) if self.maneger(sql, fetchone=True) != None else 20020927


    def make_product_sizes_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS product_sizes(
                id BIGSERIAL PRIMARY KEY,
                product_id BIGINT REFERENCES products(id),
                size VARCHAR(15),
                price NUMERIC CHECK ("price" > 0 AND "price" < 9223372036854775),
                count INTEGER,
                register_date DATE DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.maneger(sql, commit=True)


    def insert_product_sizes_table(self, product_id: int, size: str, price: int, count: int):
        sql = """
            INSERT INTO product_sizes (product_id, size, price, count)
            VALUES ('%i', '%s', '%i', '%i')
        """ % (product_id, size, price, count)
        self.maneger(sql, commit=True)


    def get_all_used_sizes_by_product_id(self, product_id):
        sql = """ SELECT size FROM product_sizes WHERE product_id='%i' """ % product_id
        return [item[0] for item in self.maneger(sql, fetchall=True)]


    def make_product_colors_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS product_color(
                id BIGSERIAL PRIMARY KEY,
                product_id BIGINT REFERENCES products(id),
                color VARCHAR(15),
                image TEXT,
                price NUMERIC CHECK ("price" > 0 AND "price" < 9223372036854775),
                count INTEGER,
                register_date DATE DEFAULT CURRENT_TIMESTAMP);
        """
        self.maneger(sql, commit=True)


    def insert_product_color_table(self, product_id: int, color: str, image: str, price: int, count: int):
        sql = """
            INSERT INTO product_color (product_id, color, image, price, count)
            VALUES ('%i', '%s', '%s', '%i', '%i') ON CONFLICT DO NOTHING;
        """ % (product_id, color, image, price, count)
        self.maneger(sql, commit=True)


    def get_all_used_colors_by_product_id(self, product_id):
        sql = """ SELECT color FROM product_color WHERE product_id='%i' """ % product_id
        return [item[0] for item in self.maneger(sql, fetchall=True)]


    def make_example_sizes_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS sizes(
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR (50) UNIQUE,
                register_date DATE DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.maneger(sql, commit=True)
    

    def insert_example_sizes_table(self, name):
        sql = """
            INSERT INTO sizes (name)
            VALUES ('%s') ON CONFLICT DO NOTHING
        """ % name
        self.maneger(sql, commit=True)

    
    def get_all_example_sizes_name(self, product_pk=None):
        if product_pk != None:
            product_id = self.get_product_id_by_product_pk(product_pk)
            used_sizes = self.get_all_used_sizes_by_product_id(product_id)
            sql = "SELECT name FROM sizes;"
            return [item[0] for item in self.maneger(sql, fetchall=True) if item[0] not in used_sizes]
        else:
            sql = "SELECT name FROM sizes;"
            return [item[0] for item in self.maneger(sql, fetchall=True)]
    
    
    def make_example_colors_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS colors (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR (50) UNIQUE,
                register_date DATE DEFAULT CURRENT_TIMESTAMP        
            )
        """
        self.maneger(sql, commit=True)


    def insert_example_colors_table(self, name):
        sql = """
            INSERT INTO colors (name)
            VALUES ('%s') ON CONFLICT DO NOTHING;
        """ % name
        self.maneger(sql, commit=True)
    
    
    def get_all_example_colors_name(self, product_pk=None):
        if product_pk != None:
            product_id = self.get_product_id_by_product_pk(product_pk)
            used_colors = self.get_all_used_colors_by_product_id(product_id)
            sql = "SELECT name FROM colors;"
            return [item[0] for item in self.maneger(sql, fetchall=True) if item[0] not in used_colors]
        else:
            sql = "SELECT name FROM colors;"
            return [item[0] for item in self.maneger(sql, fetchall=True)]
    

