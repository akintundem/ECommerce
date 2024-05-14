class User:
    def __init__(self, uid, first_name, last_name, email, password, phone):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone

    class UserBuilder:
        def __init__(self):
            self.uid = None
            self.first_name = None
            self.last_name = None
            self.email = None
            self.password = None
            self.phone = None

        def set_uid(self, uid):
            self.uid = uid
            return self

        def set_first_name(self, first_name):
            self.first_name = first_name
            return self

        def set_last_name(self, last_name):
            self.last_name = last_name
            return self

        def set_email(self, email):
            self.email = email
            return self

        def set_password(self, password):
            self.password = password
            return self

        def set_phone(self, phone):
            self.phone = phone
            return self

        def build(self):
            return User(self.uid, self.first_name, self.last_name, self.email, self.password, self.phone)

