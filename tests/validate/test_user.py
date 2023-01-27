import unittest

from validate.user import User

class UserTest(unittest.TestCase):

    def test_validate(self):
        """Test Validation that a user has an email and password."""
        http_code, error = User.validate('test@aol.com', 'test1234')
        self.assertEqual(http_code, 200)
        self.assertEqual(error, None)

        http_code, error = User.validate(None, 'test1234')
        self.assertEqual(http_code, 400)
        self.assertEqual(error, 'Missing email')

        http_code, error = User.validate('test@aol.com', None)
        self.assertEqual(http_code, 400)
        self.assertEqual(error, 'Missing password')

if __name__ == '__main__':
    unittest.main()