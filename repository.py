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
            cursor.execute("""select * from products""")
            res_execute = cursor.fetchall()
            for pr in res_execute:
                products.append(pr[0])
        return product_name in products
    
    def find_user_id(self, user_id_tg):
        with self.connection.cursor() as cursor:
            cursor.execute("""select user_id from users where user_tg_id = %s""", (user_id_tg, ))
            res = cursor.fetchone()
        return res[0]
    
    def add_product_to_backet(self, user_id, product_name, amount):
        with self.connection.cursor() as cursor:
            cursor.execute("""insert into orders (user_id, product_id, amount) values (%s, %s, %s)""", (user_id, product_name, amount))
        self.connection.commit()

        
    def show_backet(self, user_id) -> list:
        backet = []
        with self.connection.cursor() as cursor:
            cursor.execute("""select product_name from orders inner join products on orders.product_id = products.product_id""")
            res = cursor.fetchall()
        for row in res:
            backet.append(row[0])
        return backet
        
            