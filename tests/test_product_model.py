from unittest import TestCase

from app import app

from app.models.Product import Product

class TestProductModel(TestCase):
    '''
        Testing Product model
    '''

    def setUp(self):
        app.testing = True

    def test_create_product_basic(self):
        try:
            product = Product("arroz", 5.30, 3.48)
        except:
            self.fail("Exception was not expected.")
    
    def test_create_product_none_arguments(self):
        try:
            product = Product(None, 5.30, 3.48)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product("arroz", None, 3.48)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product("arroz", 5.30, None)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product(None, None, None)
            self.fail("Exception was expected.")
        except:
            pass
    
    def test_create_product_empty_string_arguments(self):
        try:
            product = Product("", 5.30, 3.48)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product("arroz", "", 3.48)
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product("arroz", 5.30, "")
            self.fail("Exception was expected.")
        except:
            pass

        try:
            product = Product("", "", "")
            self.fail("Exception was expected.")
        except:
            pass

    def test_product_string_representation(self):
        product = Product("arroz", 10.23, 9.33)
        self.assertEqual("< Product : arroz >", product.__repr__())
