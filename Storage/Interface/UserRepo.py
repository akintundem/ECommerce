class UserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def add_user(self, user):
        pass