import unittest
from termcolor import colored  # For colored test outputs
from utils import register_user

class TestAuthFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs before all tests to set up initial test data"""
        cls.test_user = {
            'first_name': 'Joh5n',
            'last_name': 'Doe',
            'username': 'Thanan1234665',  # Ensure this username is unique
            'email': 'joh45n.doe@example.com',
            'password': 'password123',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'phone_number': '1234567890'
        }

    def test_register_user(self):
        """Test user registration"""
        result = register_user(
            self.test_user['first_name'],
            self.test_user['last_name'],
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password'],
            self.test_user['date_of_birth'],
            self.test_user['gender'],
            self.test_user['phone_number']
        )
        if result:
            print(colored("User registration passed", 'green'))
        else:
            print(colored("User registration failed", 'red'))
        self.assertTrue(result, "User registration should return True for success")

if __name__ == '__main__':
    unittest.main()
