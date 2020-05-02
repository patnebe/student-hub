from src.app.models.user import User
from src.tests.base import TestSetup
import os
import random
import json

class AuthTestCase(TestSetup):
    """
    Tests to ensure the token based authentication system works as expected
    """
    def success_register_user(self):
        """A request to register a new unique user should be successful if the required input data is provided"""
        
        endpoint = '/auth/signup'
        payload = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jon.snow@winterfell.com",
            "password": "1kn0wn0th1ng"
        }

        response_object = self.client().post(endpoint, json=payload)
        
        self.assertEqual(response_object.status_code, 201)


    def test_400_error_register_user(self):
        """A request to registed a new user using incomplete data should return a 400 - bad request error"""

        endpoint = '/auth/signup'
        payloads = ["", 3, 0.3, {}, (), {"first_name": 3}, {"first_name": "John", "last_name": "Snow", "email": "s@email.com", "password": 123 }]

        for payload in payloads:
            response_object = self.client().post(endpoint, json=payload)
            response_data = json.loads(response_object.get_data())

            print(response_data)

            self.assertEqual(response_object.status_code, 400)
        
    
    def test_409_error_register_user(self):
        """A request to register a user using a previously registered email address should return a 409 - conflict error"""

        endpoint = '/auth/signup'
        payload = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jon.snow@winterfell.com",
            "password": "1kn0wn0th1ng"
        }

        first_response_object = self.client().post(endpoint, json=payload)

        second_response_object = self.client().post(endpoint, json=payload)
        
        self.assertEqual(first_response_object.status_code, 201)

        self.assertEqual(second_response_object.status_code, 409)
    


    def test_success_login_user(self):
        pass

    
    def test_401_error_login_user(self):
        pass
    


    def test_success_get_token(self):
        """
        A request for a token should be successful if the user is authorized to get a token
        """

        # Register a new user
        endpoint = '/auth/signup'
        payload = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jon.snow@winterfell.com",
            "password": "1kn0wn0th1ng"
        }

        signup_response_object = self.client().post(endpoint, json=payload)
        
        self.assertEqual(signup_response_object.status_code, 201)

        
        # Login 
        login_response_object = self.client().post('/auth/login', json={"email": "jon.snow@winterfell.com","password": "1kn0wn0th1ng"})

        login_response_data = json.loads(login_response_object.get_data())

        token = login_response_data['token']

        self.assertEqual(200, login_response_object.status_code)
        self.assertEqual(str, type(token))


        # Request a new token using the previous one as authorization
        endpoint = '/auth/token'

        response_object = self.client().get(endpoint, headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response_object.status_code, 200)

    
    def test_401_error_get_token(self):

        endpoint = '/auth/token'

        response_object = self.client().get(endpoint, headers={'Authorization': 'Bearer wrongtoken'})
        
        self.assertEqual(response_object.status_code, 401)

        login_response_object = self.client().post('/auth/login', json={"email": "jon.snow@winterfell.com","password": "1kn0wn0th1ng"})

        self.assertEqual(login_response_object.status_code, 401)



    def test_success_blacklist_token(self):
        pass



    def test_success_logout_user(self):
        pass

    def test_error_logout_user(self):
        pass