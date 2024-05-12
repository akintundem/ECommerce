import pyodbc
import csv
import json
import random

def get_connection_parameters(config_file):
    # Read the configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Get the values from the configuration file
    server = config['server']
    database = config['database']
    username = config['user']
    password = config['password']
    driver = config['driver']

    return server, database, username, password, driver


def drop_tables(cursor):
    # Define SQL queries to drop tables
    drop_queries = [
        'DROP TABLE IF EXISTS PaymentMethods;',
        'DROP TABLE IF EXISTS ShippingMethods;',
        'DROP TABLE IF EXISTS Transactions;',
        'DROP TABLE IF EXISTS Reviews;',
        'DROP TABLE IF EXISTS OrderItems;',
        'DROP TABLE IF EXISTS Orders;',
        'DROP TABLE IF EXISTS Users;',
        'DROP TABLE IF EXISTS ProductCategories;',
        'DROP TABLE IF EXISTS Products;',
        'DROP TABLE IF EXISTS Categories;'
    ]

    # Drop existing tables
    for query in drop_queries:
        cursor.execute(query)
        print(f"Dropped table: {query.split()[2]}")

def create_tables(cursor):
    # Define SQL queries for table creation
    create_queries = [
        '''CREATE TABLE Categories (
            category_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(255),
            description NVARCHAR(MAX)
        );''',
        '''CREATE TABLE Products (
            product_id VARCHAR(20) PRIMARY KEY,
            product_name NVARCHAR(255),
            discounted_price DECIMAL(10, 2),
            actual_price DECIMAL(10, 2),
            discount_percentage DECIMAL(5, 2),
            rating DECIMAL(2, 1),
            rating_count INT,
            about_product NVARCHAR(MAX),
            number_of_inventory INT,
            img_link NVARCHAR(MAX),
        );''',
        '''CREATE TABLE ProductCategories (
            product_id VARCHAR(20),
            category_id INT,
            PRIMARY KEY (product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        );''',
        '''
        CREATE TABLE Reviews (
            review_id INT IDENTITY(1,1) PRIMARY KEY,
            product_id VARCHAR(20),
            review_title NVARCHAR(255),
            review_content NVARCHAR(MAX),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );''',
        '''CREATE TABLE Users (
            user_id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(50),
            password NVARCHAR(255),
            email NVARCHAR(100),
            full_name NVARCHAR(100),
            address NVARCHAR(MAX),
            phone_number NVARCHAR(20),
            created_at DATETIME
        );''',
        '''CREATE TABLE Orders (
            order_id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT,
            order_date DATETIME,
            total_amount DECIMAL(10, 2),
            payment_status NVARCHAR(50),
            shipping_address NVARCHAR(MAX),
            payment_method NVARCHAR(50),
            transaction_id NVARCHAR(100),
            created_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );''',
        '''CREATE TABLE OrderItems (
            order_item_id INT IDENTITY(1,1) PRIMARY KEY,
            order_id INT,
            product_id VARCHAR(20),
            quantity INT,
            unit_price DECIMAL(10, 2),
            subtotal DECIMAL(10, 2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );''',
        '''CREATE TABLE Transactions (
            transaction_id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT,
            order_id INT,
            amount DECIMAL(10, 2),
            transaction_date DATETIME,
            payment_method NVARCHAR(50),
            status NVARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        );''',
        '''CREATE TABLE ShippingMethods (
            shipping_method_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50),
            description NVARCHAR(MAX)
        );''',
        '''CREATE TABLE PaymentMethods (
            payment_method_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50),
            description NVARCHAR(MAX)
        );'''
    ]

    # Create tables
    for query in create_queries:
        cursor.execute(query)
        print(f"Created table: {query.split()[2]}")

def connect_to_database(server, database, username, password, driver):
    # Connect to the database
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return conn, cursor

def insert_categories(cursor):
    with open('db/inventory.json', 'r') as file:
        data = json.load(file)
        for category in data['categories']:
            query = f"INSERT INTO Categories (name) VALUES ('{category}');"
            cursor.execute(query)

def find_categories(category):
    categories = category.split('|')
    with open('db/inventory.json', 'r') as file:
        data = json.load(file)
        indices = []
        for cat in categories:
            for index, cat_name in enumerate(data['categories']):
                if cat == cat_name:
                    indices.append(str(index))
                    break
        return ','.join(indices)

def insert_products(cursor):
    with open('db/amazon.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            product_id = row[0]
            product_name = row[1]
            discounted_price = row[3]
            actual_price = row[4]
            discount_percentage = row[5]
            rating = row[6]
            rating_count = row[7]
            about_product = row[8]
            img_link = row[15]

            query = f'''INSERT INTO Products (product_id, product_name, discounted_price, actual_price, discount_percentage, rating, rating_count, about_product, number_of_inventory, img_link)
                        VALUES ('{product_id}', '{product_name}', {discounted_price}, {actual_price}, {discount_percentage}, {rating}, {rating_count}, '{about_product}', {random.randint(0,20)}, '{img_link}');'''
            cursor.execute(query)
def insert_product_categories(cursor):
    with open('amazon.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            product_id = row[0]
            category = row[2]
            category_id = find_categories(category)
            for cat_id in category_id.split(','):
                query = f'''INSERT INTO ProductCategories (product_id, category_id)
                            VALUES ('{product_id}', '{cat_id}');'''
                cursor.execute(query)

def insert_reviews(cursor):
    with open('amazon.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            product_id = row[0]
            review_title = row[9]
            review_content = row[10]
            query = f'''INSERT INTO Reviews (product_id, review_title, review_content)
                        VALUES ('{product_id}', '{review_title}', '{review_content}');'''
            cursor.execute(query)

def insert_shipping_methods(cursor):
    with open('inventory.json', 'r') as file:
        data = json.load(file)
        for shipping_method in data['shippingmethods']:
            query = f'''INSERT INTO ShippingMethods (shipping_method_id, name, description)
                        VALUES ({shipping_method['shipping_method_id']}, '{shipping_method['title']}', '{shipping_method['description']}');'''
            cursor.execute(query)

def insert_payment_methods(cursor):
    with open('inventory.json', 'r') as file:
        data = json.load(file)
        for payment_method in data['paymentmethods']:
            query = f'''INSERT INTO PaymentMethods (payment_method_id, name, description)
                        VALUES ({payment_method['payment_method_id']}, '{payment_method['title']}', '{payment_method['description']}');'''
            cursor.execute(query)

def close_connection(conn):
    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    server, database, username, password,driver = get_connection_parameters('db/db_cred.json')
    conn, cursor = connect_to_database(server, database, username, password, driver)
    drop_tables(cursor)
    create_tables(cursor)
    insert_categories(cursor)
    insert_products(cursor)
    insert_product_categories(cursor)
    insert_reviews(cursor)
    insert_shipping_methods(cursor)
    insert_payment_methods(cursor)
    close_connection(conn)

if __name__ == "__main__":
    main()




