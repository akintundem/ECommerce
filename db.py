import pyodbc
import configparser

def read_config():
    # Read configuration from config file
    config = configparser.ConfigParser()
    config.read('/path/to/config.ini')
    return config

def get_connection_parameters(config):
    # Get database connection parameters from config file
    server = config['DATABASE']['server']
    database = config['DATABASE']['database']
    username = config['DATABASE']['username']
    password = config['DATABASE']['password']
    driver = config['DATABASE']['driver']
    return server, database, username, password, driver

def drop_tables(cursor):
    # Define SQL queries to drop tables
    drop_queries = [
        'DROP TABLE IF EXISTS Categories;',
        'DROP TABLE IF EXISTS Products;',
        'DROP TABLE IF EXISTS Users;',
        'DROP TABLE IF EXISTS Orders;',
        'DROP TABLE IF EXISTS OrderItems;',
        'DROP TABLE IF EXISTS Reviews;',
        'DROP TABLE IF EXISTS Transactions;',
        'DROP TABLE IF EXISTS ShippingMethods;',
        'DROP TABLE IF EXISTS PaymentMethods;'
    ]

    # Drop existing tables
    for query in drop_queries:
        cursor.execute(query)
        print(f"Dropped table: {query.split()[2]}")

def create_tables(cursor):
    # Define SQL queries for table creation
    create_queries = [
        '''CREATE TABLE Categories (
            category_id INT PRIMARY KEY,
            name NVARCHAR(255),
            parent_category_id INT,
            description NVARCHAR(MAX)
        );''',
        '''CREATE TABLE Products (
            product_id INT PRIMARY KEY,
            title NVARCHAR(255),
            description NVARCHAR(MAX),
            category_id INT,
            price DECIMAL(10, 2),
            stock_quantity INT,
            file_path NVARCHAR(MAX),
            file_type NVARCHAR(50),
            resolution NVARCHAR(50),
            duration INT,
            created_at DATETIME,
            updated_at DATETIME,
            is_active BIT,
            tags NVARCHAR(MAX),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        );''',
        '''CREATE TABLE Users (
            user_id INT PRIMARY KEY,
            username NVARCHAR(50),
            password NVARCHAR(255),
            email NVARCHAR(100),
            full_name NVARCHAR(100),
            address NVARCHAR(MAX),
            phone_number NVARCHAR(20),
            created_at DATETIME
        );''',
        '''CREATE TABLE Orders (
            order_id INT PRIMARY KEY,
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
            order_item_id INT PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT,
            unit_price DECIMAL(10, 2),
            subtotal DECIMAL(10, 2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );''',
        '''CREATE TABLE Reviews (
            review_id INT PRIMARY KEY,
            product_id INT,
            user_id INT,
            rating INT,
            comment NVARCHAR(MAX),
            created_at DATETIME,
            FOREIGN KEY (product_id) REFERENCES Products(product_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );''',
        '''CREATE TABLE Transactions (
            transaction_id INT PRIMARY KEY,
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
            shipping_method_id INT PRIMARY KEY,
            name NVARCHAR(50),
            description NVARCHAR(MAX),
            price DECIMAL(10, 2)
        );''',
        '''CREATE TABLE PaymentMethods (
            payment_method_id INT PRIMARY KEY,
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

def close_connection(conn):
    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    config = read_config()
    server, database, username, password, driver = get_connection_parameters(config)
    conn, cursor = connect_to_database(server, database, username, password, driver)
    drop_tables(cursor)
    create_tables(cursor)
    close_connection(conn)

if __name__ == "__main__":
    main()
