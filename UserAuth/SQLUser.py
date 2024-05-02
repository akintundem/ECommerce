class StubUserRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        self.conn.commit()

    def create_user(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone()

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()


    def update_user(self, username, new_password):
        self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        self.conn.commit()
        
    def close_connection(self):
        self.cursor.close()
        self.conn.close()
