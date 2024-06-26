import pyodbc
import csv
import json
import random

class DatabaseManager:
    def __init__(self, config_file):
        self.server, self.database, self.username, self.password, self.driver = self.get_connection_parameters(config_file)
        self.conn, self.cursor = self.connect_to_database()
        self.drop_tables()
        self.create_tables()
        self.insert_categories()
        self.insert_products()
        self.insert_product_categories()
        self.insert_reviews()
        self.insert_shipping_methods()
        self.insert_payment_methods()

    def get_connection_parameters(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        server = config['server']
        database = config['database']
        username = config['user']
        password = config['password']
        driver = config['driver']
        return server, database, username, password, driver

    def connect_to_database(self):
        conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor
    
    def get_connection_cursor(self):
        return self.conn,self.cursor
    
    def drop_tables(self):
        drop_queries = [
            'DROP TABLE IF EXISTS PaymentMethods;',
            'DROP TABLE IF EXISTS ShippingMethods;',
            'DROP TABLE IF EXISTS Transactions;',
            'DROP TABLE IF EXISTS Reviews;',
            'DROP TABLE IF EXISTS OrderItems;',
            'DROP TABLE IF EXISTS Orders;',
            'DROP TABLE IF EXISTS UserCart;',
            'DROP TABLE IF EXISTS ShoppingCart;',
            'DROP TABLE IF EXISTS Users;',
            'DROP TABLE IF EXISTS ProductCategories;',
            'DROP TABLE IF EXISTS Products;',
            'DROP TABLE IF EXISTS Categories;'
        ]
        for query in drop_queries:
            self.cursor.execute(query)
            print(f"Dropped table: {query.split()[2]}")

    def create_tables(self):
        create_queries = [
            '''CREATE TABLE Categories (
                category_id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255),
                description NVARCHAR(MAX)
            );''',
            '''CREATE TABLE Products (
                product_id VARCHAR(20) PRIMARY KEY,
                product_name NVARCHAR(MAX),
                discounted_price DECIMAL(10, 2),
                actual_price DECIMAL(10, 2),
                discount_percentage DECIMAL(5, 2),
                rating DECIMAL(2, 1),
                rating_count INT,
                about_product NVARCHAR(MAX),
                number_of_inventory INT,
                img_link NVARCHAR(MAX)
            );''',
            '''CREATE TABLE ProductCategories (
                product_id VARCHAR(20),
                category_id INT,
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
            '''
            CREATE TABLE UserCart (
                cart_id INT PRIMARY KEY IDENTITY(1,1),
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
            );''',
            '''
            CREATE TABLE ShoppingCart (
                cart_id INT,
                product_id VARCHAR(20),
                quantity INT,
                PRIMARY KEY (cart_id, product_id),  
                FOREIGN KEY (cart_id) REFERENCES UserCart(cart_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
            ''',
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
        for query in create_queries:
            self.cursor.execute(query)
            print(f"Created table: {query.split()[2]}")

    def insert_categories(self):
        with open('db/inventory.json', 'r') as file:
            data = json.load(file)
            for category in data['categories']:
                query = "INSERT INTO Categories (name) VALUES (?);"
                self.cursor.execute(query, (category,))

    def find_categories(self, category):
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

    def insert_products(self):
        with open('db/amazon.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                product_id = row[0]
                product_name = row[1]
                discounted_price = row[3].replace('₹', '').replace(',', '')
                actual_price = row[4].replace('₹', '').replace(',', '')
                discount_percentage = row[5].replace('%', '')
                rating = row[6].replace("|", "0")
                rating_count = row[7].replace(',', '')
                about_product = row[8]
                img_link = row[15]
                query = "SELECT COUNT(*) FROM Products WHERE product_id = ?"
                self.cursor.execute(query, (product_id,))
                result = self.cursor.fetchone()
                if result[0] > 0:
                    continue
                query = '''INSERT INTO Products (product_id, product_name, discounted_price, actual_price, discount_percentage, rating, rating_count, about_product, number_of_inventory, img_link)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                self.cursor.execute(query, (product_id, product_name, discounted_price, actual_price, discount_percentage, rating, rating_count, 'hello', random.randint(0,20), img_link))

    def insert_product_categories(self):
        with open('db/amazon.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                product_id = row[0]
                category = row[2]
                category_id = self.find_categories(category)
                for cat_id in category_id.split(','):
                    query = '''INSERT INTO ProductCategories (product_id, category_id)
                                VALUES (?, ?);'''
                    self.cursor.execute(query, (product_id, int(cat_id)+1))

    def insert_reviews(self):
        with open('db/amazon.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                product_id = row[0]
                review_title = row[9]
                review_content = row[10]
                query = '''INSERT INTO Reviews (product_id, review_title, review_content)
                            VALUES (?, ?, ?);'''
                self.cursor.execute(query, (product_id, review_title, review_content))

    def insert_shipping_methods(self):
        with open('db/inventory.json', 'r') as file:
            data = json.load(file)
            for shipping_method in data['shippingmethods']:
                query = '''INSERT INTO ShippingMethods (name, description)
                            VALUES (?, ?);'''
                self.cursor.execute(query, (shipping_method['name'], shipping_method['description']))

    def insert_payment_methods(self):
        with open('db/inventory.json', 'r') as file:
            data = json.load(file)
            for payment_method in data['paymentmethods']:
                query = '''INSERT INTO PaymentMethods (name, description)
                            VALUES (?, ?);'''
                self.cursor.execute(query, (payment_method['title'], payment_method['description']))

    def get_products(self):
        query = "SELECT TOP 10 * FROM Products;"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        products = []
        for row in rows:
            product = {
                'product_id': row[0],
                'product_name': row[1],
                'discounted_price': float(row[2]),
                'actual_price': float(row[3]),
                'discount_percentage': float(row[4]),
                'rating': float(row[5]),
                'rating_count': int(row[6]),
                'about_product': row[7],
                'number_of_inventory': int(row[8]),
                'img_link': row[9]
            }
            products.append(product)
        return json.dumps(products)

    def search_by_category(self, category):
        query = '''
            SELECT p.product_id, p.product_name, p.discounted_price, p.actual_price, p.discount_percentage, p.rating, p.rating_count, p.about_product, p.number_of_inventory, p.img_link
            FROM Products p
            INNER JOIN ProductCategories pc ON p.product_id = pc.product_id
            INNER JOIN Categories c ON pc.category_id = c.category_id
            WHERE c.name = ?
        '''
        self.cursor.execute(query, (category,))
        rows = self.cursor.fetchall()
        products = []
        for row in rows:
            product = {
                'product_id': row[0],
                'product_name': row[1],
                'discounted_price': float(row[2]),
                'actual_price': float(row[3]),
                'discount_percentage': float(row[4]),
                'rating': float(row[5]),
                'rating_count': int(row[6]),
                'about_product': row[7],
                'number_of_inventory': int(row[8]),
                'img_link': row[9]
            }
            products.append(product)
        return json.dumps(products)

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    