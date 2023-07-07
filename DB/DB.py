import psycopg2
from psycopg2 import OperationalError
from multipledispatch import dispatch

class Person:
    def __init__(self, name: str, number_phone: str, adress: str, telegram_id: int):
        self.name = name
        client = Client()
        self.wish_list = client.view_wish_list(telegram_id=telegram_id)
        self.number_phone = number_phone
        self.adress = adress
        self.telegram_id = telegram_id

    def get_params(self) -> dict:
        return \
            {
                'name': self.name,
                'wish_list': self.wish_list,
                'number_phone': self.number_phone,
                'adress': self.adress,
                'telegram_id' : self.telegram_id,
            }


class Wish_list:
    def __init__(self, id: int, product_id: str,telegram_id: int):
        self.id = id,
        self.product_id = product_id
        self.telegram_id = telegram_id

    def get_params(self) -> dict:
        return {
            'id': self.id,
            'product': self.product,
            'telegram_id': self.telegram_id,
        }


class Product:
    def __init__(self, id: int, name: str, category: str, description: str, manufacturer: str, prise: float):
        self.id = id,
        self.name = name,
        self.category = category,
        self.description = description,
        self.manufacturer = manufacturer,
        self.prise = prise,

    def get_params(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'prise': self.prise,
        }


class Manufacturer:
    def __init__(self, id: int, name: str, description: str, product_list: list):
        self.id = id,
        self.name = name,
        self.description = description,
        self.product_list = product_list,

    def get_params(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_list': self.product_list,
        }


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(database=db_name,user=db_user,password=db_password,host=db_host,port=db_port,)
        print("Соеденине успешно")
    except:
        connection = psycopg2.connect(database="postgres",user=db_user,password=db_password,host=db_host,port=db_port,)
        connection.autocommit = True
        cursor = connection.cursor()
        create_database(connection, "CREATE DATABASE shop")
        print("База данных shop созданна")
        create_connection("shop", "postgres", "123", "127.0.0.1", "5432")
        print("Подключено к бд shop")
    return connection

def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Запрос выполнен")
    except OperationalError as e:
        print(f"Ошибка '{e}'")

tab = {
    'Person': "CREATE TABLE IF NOT EXISTS Person (id SERIAL PRIMARY KEY,name TEXT,number_phone TEXT,adress TEXT, telegram_id INT);",
    'Wish_list': "CREATE TABLE IF NOT EXISTS wish_list (id SERIAL PRIMARY KEY,product_id int NOT NULL,telegram_id INTEGER NOT NULL);",
    'Product': "CREATE TABLE IF NOT EXISTS product (id SERIAL PRIMARY KEY,name TEXT NOT NULL,category TEXT,description TEXT,manufacturer TEXT,prise FLOAT);",
    'Manufacturer': "CREATE TABLE IF NOT EXISTS manufacturer(id SERIAL PRIMARY KEY, name TEXT NOT NULL,description TEXT);"
}

class Client:
    def __init__(self) -> None:
        self.connection = create_connection("shop", "postgres", "123", "127.0.0.1", "5432")
        self.cursor = self.connection.cursor()
    
    def check(self) -> None:
        for v in tab.values():
            self.cursor.execute(v)
            self.connection.commit()

    def add_Person(self,name:str,number_phone:str,adress:str,telegram_id:int):
        self.cursor.execute(f"insert into person (name,number_phone,adress) values ('{name}','{number_phone}','{adress}','{telegram_id}');")
        self.connection.commit()
        print("Запись добавлена в Person")
    
    def add_to_Wish_list(self,product_id:int,telegram_id:int):
        self.cursor.execute(f"insert into wish_list (product_id,telegram_id) values ('{product_id}',{telegram_id});")
        self.connection.commit()
        print("Запись добавлена в Wish list")
    
    def add_Product(self,name:str,category:str,description:str,manufacturer:str,prise:float):
        self.cursor.execute(f"insert into product (name,category,description,manufacturer,prise) values ('{name}','{category}','{description}','{manufacturer}',{prise});")
        self.connection.commit()
        print("Запись добавлена в Product")        
    
    def add_Manufacturer(self,name:str,description:str):
        self.cursor.execute(f"insert into manufacturer (name,description,product_list) values ('{name}','{description}');")
        self.connection.commit()
        print("Запись добавлена в Manufacturer")       
    
    @dispatch(int)
    def clear_trash(self,telegram_id:int):
        self.cursor.execute(f"delete from wish_list where telegram_id = {telegram_id};")
        return self.connection.commit()
    
    @dispatch(int,int)
    def clear_trash(self,telegram_id:int,product_id:int):
        self.cursor.execute(f"delete from wish_list where telegram_id = {telegram_id} AND product_id = {product_id};")
        return self.connection.commit()
    
    def count_product(self,name:str):
        self.cursor.execute(f"Select Count(*) from product where name = '{name}'")
        return self.cursor.fetchall()

    #########################################################
    def view_wish_list(self,telegram_id:int):
        self.cursor.execute(f"Select product.name, wish_list.telegram_id from wish_list,product where product.id = wish_list.product_id AND telegram_id = '{telegram_id}';")
        return self.cursor.fetchall()

    def view_all(self,table:str):
        self.cursor.execute(f"Select * from {table};")
        return self.cursor.fetchall()
    
    def find_params(self,table:str,colum:str,param_value):
        self.cursor.execute(f"Select * from {table} where {colum} LIKE '%{param_value}%;'")
        return self.cursor.fetchall()
    

