import pyodbc

class SQLUserRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

        def create_table(self):
            self.cursor.execute('CREATE TABLE users (id INT IDENTITY(1,1) PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)')
            self.conn.commit()
        def create_user(self, username, password):
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()

        def find_user(self, username):
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = self.cursor.fetchone()
            return user

        
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

def main():
    # Connect to the Docker SQL Server
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1433;DATABASE=master;UID=sa;PWD=Iamayokakfwesh1.')
    
    # Create an instance of the StubUserRepository
    user_repo = SQLUserRepository(conn)
    
    # Example usage:
    # Create a new user
    user_repo.create_user('john_doe', 'password123')

    # Retrieve user by email (assuming email is unique)
    user = user_repo.get_user_by_email('john_doe@example.com')
    print(user)

    # Update user's password
    user_repo.update_user('john_doe', 'new_password')

    # Delete user
    user_repo.delete_user('john_doe')
    
    # Close the connection
    user_repo.close_connection()

if __name__ == "__main__":
    main()
