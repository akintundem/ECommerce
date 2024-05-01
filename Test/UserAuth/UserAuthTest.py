import unittest

from UserAuthentication.UserAuth import UserAuth

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.user_auth = UserAuth()
        self.user_auth.register_user("test@example.com", "password123", "Test User", "123 Main St", "Credit Card")

    def test_register_user(self):
        self.assertTrue(self.user_auth.register_user("newuser@example.com", "newpassword123", "New User", "456 Second St", "PayPal"))

    def test_login_user(self):
        self.assertTrue(self.user_auth.login_user("test@example.com", "password123"))
        self.assertFalse(self.user_auth.login_user("test@example.com", "wrongpassword"))

    def test_reset_password(self):
        self.assertTrue(self.user_auth.reset_password("test@example.com", "newpassword123"))
        self.assertTrue(self.user_auth.login_user("test@example.com", "newpassword123"))

if __name__ == "__main__":
    unittest.main()
