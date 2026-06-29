import psycopg2
import datetime

class PostgresRepository:
    def __init__(self, name, ip, password):
        self.connection = psycopg2.connect(f"dbname='{name}' user='postgres' host='{ip}' password='{password}'")
    

    def add_user(self, tg_id):
        with self.connection.cursor() as cursor:
            current_date = datetime.datetime.now()
            cursor.execute("""insert into users (user_tg_id, data_reg) values (%s, %s) """, (tg_id, current_date))
        self.connection.commit()
        
    
    def is_registrated(self, tg_id) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute("""select * from users where user_tg_id = %s""", (tg_id, ))
            res_execution = cursor.fetchone()
        return res_execution is not None
            

    def is_admin(self, tg_id) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute("""select user_tg_id from users inner join admins on admins.admin_id = users.user_id where user_tg_id = %s""", (tg_id, ))
            res_execute = cursor.fetchone()
        return res_execute is not None
    

    def is_product_avaliable(self, product_name) -> list:
        products = []
        with self.connection.cursor() as cursor:
            cursor.execute("""select product_name from products""")
            res_execute = cursor.fetchall()
            for pr in res_execute:
                products.append(pr[0])
        return product_name in products
    
    def find_user_id(self, user_id_tg):
        with self.connection.cursor() as cursor:
            cursor.execute("""select user_id from users where user_tg_id = %s""", (user_id_tg, ))
            res = cursor.fetchone()
        return res[0] if res is not None else False
    
    def find_product_id(self, product_name):
        with self.connection.cursor() as cursor:
            cursor.execute("""select product_id from products where product_name = %s""", (product_name, ))
            res= cursor.fetchone()
        return res[0]

    def add_product_to_backet(self, user_id, product_id, amount):
        with self.connection.cursor() as cursor:
            cursor.execute("""insert into orders (user_id, product_id, amount) values (%s, %s, %s)""", (user_id, product_id, amount))
        self.connection.commit()

        
    def show_backet(self, user_id) -> dict:
        backet = {} # {name: (price, amount)}
        with self.connection.cursor() as cursor:
            cursor.execute("""select product_name, price, amount  from orders inner join products on orders.product_id = products.product_id where orders.user_id = %s""", (user_id, ))
            res = cursor.fetchall()
        for row in res:
            backet[row[0]] = (row[1], row[2])
        return backet
        

    def get_users(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("""select user_id, user_tg_id, data_reg from users""")
            res = cursor.fetchall()
        return res

    def get_user(self, user_id) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("""select user_id, user_tg_id, data_reg from users where user_id = %s""", (user_id, ))
            res = cursor.fetchone()
        return res

    def get_admins(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("""select admin_id from admins """)
            res = cursor.fetchall()
        return [id[0] for id in res]
            

    def add_product(self, name, price):
        with self.connection.cursor() as cursor:
            cursor.execute("""insert into products (product_name, price) values (%s, %s)""", (name, price))
        self.connection.commit()

    def get_admins_tgid(self):
        admin_tgids = []
        for admin_id in self.get_admins():
            admin_tgids.append(self.get_user(admin_id)[1])
        
        return admin_tgids
    

    def get_cities(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("""select city_name from cities;""")
            res = cursor.fetchall()
        return [city[0] for city in res]
    
    def get_roads(self, city_from):
        roads_forcityfrom = {}
        
        cursor = self.connection.cursor()

        cursor.execute("""select cities_to.city_name, distance from roads
                       inner join cities cities_to on roads.city_to = cities_to.city_id 
                       inner join cities cities_from on roads.city_from = cities_from.city_id where cities_from.city_name = %s""", (city_from, ))

        for string in cursor.fetchall():
            roads_forcityfrom[string[0]] = string[1]
        return roads_forcityfrom
    
    def delete_backet(self, user_tg_id):
        with self.connection.cursor() as cursor: 
            cursor.execute("""delete from orders where user_id = (select user_id from users where user_tg_id = %s)""", (user_tg_id, ))
        self.connection.commit()