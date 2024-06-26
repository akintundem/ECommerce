class StubUserRepository:
    def __init__(self):
        self.users = []

    def create_user(self, user):
        self.users.append(user)
        return True

    def get_user_by_email(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def delete_user(self, username):
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
                return True
        return False
    
    def update_user(self, username, new_password):
        for user in self.users:
            if user.username == username:
                user.password = new_password
                return True
        return False
    
    def close_connection(self):
        pass