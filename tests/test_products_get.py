import os
from unittest import TestCase

from flask import Response

from app import app, db

class TestProductsGet(TestCase):
    '''
        Testing GET method of the products resource
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

        # Requests for test
        self.response = self.test_app.get('/products')
        self.auth_response = self.test_app.get('/products', headers={"authorization": f"Bearer {self.token}"})
        self.auth_response_no_bearer = self.test_app.get('/products', headers={"authorization": self.token})
        self.auth_response_invalid = self.test_app.get('/products', headers={"authorization": "Bearer 382adhhd"})

    def tearDown(self):
        # Ending the database session
        db.session.remove()

        # Dropping all sqlite data
        db.drop_all()

        # Removing existing database file
        os.unlink('tests/testing.db')

    ### Testing authenticated

    def test_get_all_products_with_authentication_return_status_200(self):
        self.assertEqual(200, self.auth_response.status_code)
    
    def test_get_all_products_with_authentication_return_json(self):
        self.assertEqual('application/json', self.auth_response.content_type)
    
    ### Testing unauthenticated

    def test_get_all_products_without_authentication_return_status_401(self):
        self.assertEqual(401, self.response.status_code)
    
    def test_get_all_products_without_authentication_return_json(self):
        self.assertEqual('application/json', self.response.content_type)

    def test_get_all_products_without_authentication_return_error_not_authorized(self):
        self.assertEqual({"error": "Not authorized."}, self.response.json)
    
    def test_get_all_products_with_authentication_and_token_without_bearer_prefix_return_status_401(self):
        self.assertEqual(401, self.auth_response_no_bearer.status_code)
    
    def test_get_all_products_with_authentication_and_token_without_bearer_prefix_return_json(self):
        self.assertEqual('application/json', self.auth_response_no_bearer.content_type)

    def test_get_all_products_with_authentication_and_token_without_bearer_prefix_return_error_invalid_token(self):
        self.assertEqual({"error": "Invalid token."}, self.auth_response_no_bearer.json)
    
    def test_get_all_products_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_status_401(self):
        self.assertEqual(401, self.auth_response_invalid.status_code)

    def test_get_all_products_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_json(self):
        self.assertEqual('application/json', self.auth_response_invalid.content_type)
    
    def test_get_all_products_with_authentication_and_token_with_bearer_prefix_but_without_valid_token_return_error_invalid_token(self):
        self.assertEqual({"error": "Invalid token."}, self.auth_response_invalid.json)
