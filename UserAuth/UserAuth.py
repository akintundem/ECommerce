
from .User import User
import bcrypt  
from .UserValidation import UserValidation

class UserAuth:

    def register_user(self, first_name, last_name, email, password, phone, user_storage):
        user_validation = UserValidation()
        if not user_validation.validate_user_input_in_registration(first_name, last_name, email, password, phone):
            return False, "Invalid user input"

        try:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # Generate hashed password
            user_builder = User.UserBuilder().set_email(email).set_password(hashed_password).set_first_name(first_name).set_last_name(last_name).set_phone(phone)
            user = user_builder.build()
            if user_storage.create_user(user):
                return True, "User registered successfully"
            else:
                return False, "Failed to register user"
        except Exception as e:
            print(f"Error registering user: {str(e)}")
            return False, "An error occurred during registration"


    def login_user(self, email, password, user_storage):
        user_validation = UserValidation()
        if not user_validation.validate_user_input_in_login(email, password):
            return False
        user = user_storage.get_user_by_email(email)
        if not user:
            return False
        try:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error logging in user: {str(e)}")
            return False

    def reset_password(self, email, old_password, new_password, user_storage):
        user_validation = UserValidation()
        if not user_validation.validate_user_input_in_reset_password(email, old_password, new_password):
            return False
        
        user = user_storage.get_user_by_email(email)
        if not user:
            return False

        try:
            if bcrypt.checkpw(old_password.encode(), user.password.encode()):
                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                user.password = hashed_password
                return True
            else:
                return False
        except Exception as e:
            print(f"Error resetting password: {str(e)}")
            return False