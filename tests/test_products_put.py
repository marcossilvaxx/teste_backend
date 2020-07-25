import os
from unittest import TestCase

from flask import Response

from app import app, db

class TestProductsPut(TestCase):
    '''
        Testing PUT method of the products resource
    '''

    def setUp(self):
        app.testing = True

        # Creating SQLite database ONLY FOR TEST PURPOSES
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/testing.db'
        db.create_all()

        self.test_app = app.test_client()

        # Registering fake user for test
        self.test_app.post('/auth/register', json={"name": "marcos", "email": "marcos@email.com", "password": "12345"})

        # Authenticating fake user for test
        self.token = Response(self.test_app.post('/auth/login', json={"email": "marcos@email.com", "password": "12345"})).response.json['token']

        # Fake product for test
        test_product = {"name": "feijão", "price": 8.80, "cost": 5.15}

        # Registering fake product for test
        self.test_app.post('/products', json=test_product, headers={"authorization": f"Bearer {self.token}"})

        # Fake updated products for test
        test_product_updated_1 = {"name": "arroz", "price": 10.55, "cost": 4.45}
        test_product_updated_2 = {"name": "macarrão", "price": 12.15}
        test_product_updated_3 = {"name": "carne"}
        test_product_updated_4 = {}

        # Requests for test
        self.response = self.test_app.put('/products/1', json=test_product_updated_1)
        self.auth_response = self.test_app.put('/products/1', json=test_product_updated_1, headers={"authorization": f"Bearer {self.token}"})
        self.auth_response2 = self.test_app.put('/products/1', json=test_product_updated_2, headers={"authorization": f"Bearer {self.token}"})
        self.auth_response3 = self.test_app.put('/products/1', json=test_product_updated_3, headers={"authorization": f"Bearer {self.token}"})
        self.auth_response4 = self.test_app.put('/products/1', json=test_product_updated_4, headers={"authorization": f"Bearer {self.token}"})
        self.auth_response5 = self.test_app.put('/products/2', json=test_product_updated_1, headers={"authorization": f"Bearer {self.token}"})
        self.auth_response_no_bearer = self.test_app.put('/products/1', json=test_product_updated_1, headers={"authorization": self.token})
        self.auth_response_invalid = self.test_app.put('/products/1', json=test_product_updated_1, headers={"authorization": "Bearer 382adhhd"})

    def tearDown(self):
        # Ending the database session
        db.session.remove()

        # Dropping all sqlite data
        db.drop_all()

        # Removing existing database file
        os.unlink('tests/testing.db')

    ### Testing authenticated

    def test_put_product_updating_all_fields_with_authentication_return_status_200(self):
        self.assertEqual(200, self.auth_response.status_code)
    
    def test_put_product_updating_all_fields_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response.content_type)

    def test_put_product_updating_all_fields_with_authentication_return_product_was_updated(self):
        self.assertEqual({ "message": "Product was updated" }, self.auth_response.json)
    
    def test_put_product_updating_two_fields_with_authentication_return_status_200(self):
        self.assertEqual(200, self.auth_response2.status_code)
    
    def test_put_product_updating_two_fields_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response2.content_type)
    
    def test_put_product_updating_two_fields_with_authentication_return_product_was_updated(self):
        self.assertEqual({ "message": "Product was updated" }, self.auth_response2.json)

    def test_put_product_updating_one_field_with_authentication_return_status_200(self):
        self.assertEqual(200, self.auth_response3.status_code)
    
    def test_put_product_updating_one_field_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response3.content_type)
    
    def test_put_product_updating_one_field_with_authentication_return_product_was_updated(self):
        self.assertEqual({ "message": "Product was updated" }, self.auth_response3.json)
    
    def test_put_product_updating_without_fields_with_authentication_return_status_400(self):
        self.assertEqual(400, self.auth_response4.status_code)
    
    def test_put_product_updating_without_fields_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response4.content_type)
    
    def test_put_product_updating_without_fields_with_authentication_return_error_bad_request(self):
        self.assertEqual({ "error": "Bad request. Updating without fields." }, self.auth_response4.json)

    def test_put_product_nonexistent_with_authentication_return_status_404(self):
        self.assertEqual(404, self.auth_response5.status_code)
    
    def test_put_product_nonexistent_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response5.content_type)
    
    def test_put_product_nonexistent_with_authentication_return_error_product_not_found(self):
        self.assertEqual({ "error": "Product not found." }, self.auth_response5.json)

    ### Testing unauthenticated

    def test_put_product_without_authentication_return_status_401(self):
        self.assertEqual(401, self.response.status_code)
    
    def test_put_product_without_authentication_return_json(self):
        self.assertEqual('application/json', self.response.content_type)

    def test_put_product_without_authentication_return_error_not_authorized(self):
        self.assertEqual({"error": "Not authorized."}, self.response.json)
    
    def test_put_product_with_authentication_and_token_without_bearer_prefix_return_status_401(self):
        self.assertEqual(401, self.auth_response_no_bearer.status_code)
    
    def test_put_product_with_authentication_and_token_without_bearer_prefix_return_json(self):
        self.assertEqual('application/json', self.auth_response_no_bearer.content_type)

    def test_put_product_with_authentication_and_token_without_bearer_prefix_return_error_invalid_token(self):
        self.assertEqual({"error": "Invalid token."}, self.auth_response_no_bearer.json)
    
    def test_put_product_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_status_401(self):
        self.assertEqual(401, self.auth_response_invalid.status_code)

    def test_put_product_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_json(self):
        self.assertEqual('application/json', self.auth_response_invalid.content_type)
    
    def test_put_product_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_error_invalid_token(self):
        self.assertEqual({"error": "Invalid token."}, self.auth_response_invalid.json)
