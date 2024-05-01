from UserAuthentication.User import User
import bcrypt  

class UserAuth:

    def register_user(self, first_name, last_name, email, password, phone, user_storage):
        if self.get_user_by_email(email, user_storage):
            return False
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        user_builder = User.Builder().set_email(email).set_password(hashed_password).set_first_name(first_name).set_last_name(last_name).set_phone(phone)
        user = user_builder.build()
        return user_storage.append(user)
        

    def login_user(self, email, password, user_storage):
        user = self.get_user_by_email(email,user_storage)
        if not user:
            return False
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return True
        else:
            return False

    def reset_password(self, email, new_password, user_storage):
        user = self.get_user_by_email(email, user_storage)
        if not user:
            return False
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()  # Hashing the new password
        user.password = hashed_password
        return True
