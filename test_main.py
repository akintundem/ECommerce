import unittest
from unittest.mock import MagicMock
from UserAuth.StubUser import StubUserRepository
from UserAuth.UserAuth import UserAuth

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.user_storage = StubUserRepository()
        self.user_auth = UserAuth()

    def test_register_user(self):
        # Test registering a new user
        registered = self.user_auth.register_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            phone="1234567890",
            user_storage=self.user_storage
        )
        self.assertTrue(registered)
        self.assertEqual(len(self.user_storage.users), 1)

        # Test registering a user with an existing email
        registered = self.user_auth.register_user(
            first_name="Jane",
            last_name="Smith",
            email="john@example.com",
            password="password456",
            phone="9876543210",
            user_storage=self.user_storage
        )
        self.assertFalse(registered)
        self.assertEqual(len(self.user_storage.users), 1)

    def test_login_user(self):
        # Test logging in with valid credentials
        self.user_storage.add_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            phone="1234567890"
        )
        logged_in = self.user_auth.login_user(
            email="john@example.com",
            password="password123",
            user_storage=self.user_storage
        )
        self.assertTrue(logged_in)

        # Test logging in with invalid email
        logged_in = self.user_auth.login_user(
            email="jane@example.com",
            password="password123",
            user_storage=self.user_storage
        )
        self.assertFalse(logged_in)

        # Test logging in with invalid password
        logged_in = self.user_auth.login_user(
            email="john@example.com",
            password="wrongpassword",
            user_storage=self.user_storage
        )
        self.assertFalse(logged_in)

    def test_reset_password(self):
        # Test resetting password for an existing user
        self.user_storage.add_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            phone="1234567890"
        )
        reset_password = self.user_auth.reset_password(
            email="john@example.com",
            new_password="newpassword123",
            user_storage=self.user_storage
        )
        self.assertTrue(reset_password)

        # Test resetting password for a non-existing user
        reset_password = self.user_auth.reset_password(
            email="jane@example.com",
            new_password="newpassword123",
            user_storage=self.user_storage
        )
        self.assertFalse(reset_password)

if __name__ == "__main__":
    unittest.main()