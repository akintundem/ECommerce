import re

class UserValidation:
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    PHONE_REGEX = r'^\d{10}$'
    NAME_REGEX = r'^[a-zA-Z\'\- ]+$'

    def validate_user_input_in_registration(self, first_name, last_name, email, password, phone):
        if not self.validate_name(first_name):
            return False
        if not self.validate_name(last_name):
            return False
        if not self.validate_email(email):
            return False
        if not self.validate_password(password):
            return False
        if not self.validate_phone(phone):
            return False
        return True

    def validate_user_input_in_login(self, email, password):
        if not self.validate_email(email):
            return False
        if not self.validate_password(password):
            return False
        return True
    
    def validate_user_input_in_reset_password(self, email, old_password, new_password):
        if not self.validate_email(email):
            return False
        if not self.validate_password(old_password):
            return False
        if not self.validate_password(new_password):
            return False
        return True 
       
    def validate_name(self, name):
        return bool(re.match(self.NAME_REGEX, name))

    def validate_email(self, email):
        return bool(re.match(self.EMAIL_REGEX, email))

    def validate_password(self, password):
        return bool(re.match(self.PASSWORD_REGEX, password))

    def validate_phone(self, phone):
        return bool(re.match(self.PHONE_REGEX, phone))
