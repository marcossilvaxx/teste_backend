from unittest import TestCase

from werkzeug.security import generate_password_hash, check_password_hash

from app import app

from app.models.User import User

class TestUserModel(TestCase):
    '''
        Testing User model
    '''

    def setUp(self):
        app.testing = True

    def test_create_user_basic(self):
        try:
            user = User("marcos", "marcos@email.com", "12345")
        except:
            self.fail("Exception was not expected.")
    
    def test_create_user_none_arguments(self):
        try:
            user = User(None, "marcos@email.com", "12345")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User("marcos", None, "12345")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User("marcos", "marcos@email.com", None)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User(None, None, None)
            self.fail("Exception was expected.")
        except:
            pass
    
    def test_create_user_empty_strings_arguments(self):
        try:
            user = User("", "marcos@email.com", "12345")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User("marcos", "", "12345")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User("marcos", "marcos@email.com", "")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            user = User("", "", "")
            self.fail("Exception was expected.")
        except:
            pass

    def test_create_user_generate_password_hash(self):
        user = User("marcos", "marcos@email.com", "12345")
        self.assertTrue(check_password_hash(user.password, "12345"))

    def test_user_verify_password_basic(self):
        user = User("marcos", "marcos@email.com", "12345")
        self.assertTrue(user.verify_password("12345"))
    
    def test_user_verify_password_none_argument(self):
        try:
            user = User("marcos", "marcos@email.com", "12345")
            user.verify_password(None)
            self.fail("Exception was expected.")
        except:
            pass
    
    def test_user_verify_password_empty_string_argument(self):
        try:
            user = User("marcos", "marcos@email.com", "12345")
            user.verify_password("")
            self.fail("Exception was expected.")
        except:
            pass

    def test_user_string_representation(self):
        user = User("marcos", "marcos@email.com", "12345")
        self.assertEqual("< User : marcos >", user.__repr__())
