from repository import PostgresRepository 
import dotenv
import os
import csv
dotenv.load_dotenv()

name = os.getenv('dbname')
ip = os.getenv('dbhost')
password = os.getenv('dbpassword')

db = PostgresRepository(ip=ip, name=name, password=password)
connection = db.connection
# with open('products.csv', 'r', encoding='UTF-8') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         db.add_product(row['name'], row['price'])


with open('cities.csv', 'r', encoding='UTF-8') as file:
    reader = csv.DictReader(file)
    with connection.cursor() as cursor:
        added_cities = []
        for road in reader:
            if road['dest1'] not in added_cities:
                added_cities.append(road['dest1'])
                cursor.execute('insert into cities (city_name) values (%s)', (road["dest1"],))
            if road['dest2'] not in added_cities:
                added_cities.append(road['dest2'])
                cursor.execute('insert into cities (city_name) values (%s)', (road['dest2'],))
    connection.commit()


# заполнение таблицы roads
with open('cities.csv', 'r', encoding='UTF-8') as file:
    reader = csv.DictReader(file)
    with connection.cursor() as cursor:

        for road in reader:
            cursor.execute('insert into roads (city_from, city_to, distance) values ((select city_id from cities where city_name = %s), (select city_id from cities where city_name = %s), %s)', (road['dest1'], road['dest2'], road['time'], ))
        connection.commit()
    connection.commit()