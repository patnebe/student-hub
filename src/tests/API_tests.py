from src.app.models.user import User
from src.tests.base import TestSetup
import os
import random
import json
import requests
import pytest


class NanodegreeTestCase(TestSetup):
    """Test cases to ensure that CRUD operations on the Nanodegree model work as expected"""

    invalid_random_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    def get_auth_token_from_Auth0(self, client_id=None, client_secret=None):
        """
        This returns an auth0 token for the provided login credentials
        """

        AUTH0_TENANT_DOMAIN = os.getenv('AUTH0_TENANT_DOMAIN')

        url = f'https://{AUTH0_TENANT_DOMAIN}/oauth/token'

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": os.getenv('AUTH0_API_AUDIENCE'),
            "grant_type": "client_credentials"
        }

        response_object = requests.post(url=url, json=payload)

        response_data = response_object.json()

        if "access_token" in response_data and "token_type" in response_data:
            return response_data['access_token']

        return None

    def create_nanodegree_request(self, auth_token=None, nanodegree_details={}):
        """
        Helper method for creating nanodegrees

        Returns the http response object
        """

        endpoint = "api/v1/nanodegrees"

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response_object = self.client().post(
            endpoint, headers=headers, json=nanodegree_details)

        return response_object

    def create_project_request(self, auth_token=None, nanodegree_id=None, list_of_projects=[]):
        """
        Helper method for creating nanodegree projects

        Returns the http response object
        """
        endpoint = f"api/v1/nanodegrees/{nanodegree_id}/projects"

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        payload = {"projects": list_of_projects}

        response_object = self.client().post(
            endpoint, headers=headers, json=payload)

        return response_object

    def test_201_success_create_nanodegree(self):
        """
        A request by an admin to create a nanodegree should return a 201 status code
        """

        # Retreive login credentials
        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        # Get auth token with sufficient authorization (Admin role) from auth0 endpoint
        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        # Utilize the auth0 token to create a nanodegree
        payload = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=payload)

        response_body = response_object.get_json()

        nanodegree_data = response_body['data']

        self.assertEqual(response_object.status_code, 201)
        self.assertEqual(type(nanodegree_data), dict)
        self.assertTrue('title' in nanodegree_data,
                        'The key "title" is missing in the data object')
        self.assertTrue('description' in nanodegree_data,
                        'The key "description" is missing in the data object')
        self.assertTrue('id' in nanodegree_data,
                        'The key "id" is missing in the data object')

    def test_400_error_create_nanodegree(self):
        """
        A request to create a nanodegree should return a 400 error if the request payload is not properly formatted
        """
        # Retreive login credentials
        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        # Get auth token with sufficient authorization (Admin role) from auth0 endpoint
        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        # Utilize the auth0 token to create a nanodegree
        list_of_payloads = [{
            "description": "None for now"
        }, {}, 1, "invalid string payload", []]

        for payload in list_of_payloads:
            response_object = self.create_nanodegree_request(
                auth_token=admin_token, nanodegree_details=payload)

            response_body = response_object.get_json()

            self.assertEqual(response_object.status_code, 400)

    def test_401_error_create_nanodegree(self):
        """
        A request to create a nanodegree by an invalid user should return a 401 status code
        """

        payload = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=self.invalid_random_token, nanodegree_details=payload)

        self.assertEqual(response_object.status_code, 401)

    def test_403_error_create_nanodegree(self):
        """
        A request to create a nanodegree by an authenticated user who is not an admin should return a 403 status code
        """

        # Retreive login credentials
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        # Get auth token with insufficient authorization (student role) from auth0 endpoint
        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        # Utilize the auth0 token to create a nanodegree
        payload = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=student_token, nanodegree_details=payload)

        self.assertEqual(response_object.status_code, 403)

    def test_200_success_get_nanodegrees(self):
        """
        A GET request to /nanodegrees should return a list of all the available nanodegrees
        """

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        payload_one = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        payload_two = {
            "title": "Data Engineer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=payload_one)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=payload_two)

        endpoint = 'api/v1/nanodegrees'

        response_object = self.client().get(endpoint)
        response_body = response_object.get_json()

        self.assertEqual(response_object.status_code, 200)
        list_of_nanodegrees = response_body['data']

        self.assertEqual(type(list_of_nanodegrees), list)

        for nanodegree in list_of_nanodegrees:
            self.assertTrue('title' in nanodegree,
                            'The key "title" is missing in the data object')
            self.assertTrue('description' in nanodegree,
                            'The key "description" is missing in the data object')
            self.assertTrue('id' in nanodegree,
                            'The key "id" is missing in the data object')

    def test_201_success_create_nanodegree_projects(self):
        """
        A POST request to /nanodegree/<int:id>/projects should return a 201 success and all the projects for the specified nanodegree
        """
        # create a nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"},
            {"title": "Coffee Shop Fullstack"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # make a call to the projects endpoint to get a list of projects
        endpoint = f'api/v1/nanodegrees/{nanodegree_id}/projects'

        response_object = self.client().get(endpoint)

        self.assertEqual(response_object.status_code, 200)

        list_of_nanodegree_projects = response_object.get_json()['data']

        self.assertEqual(type(list_of_nanodegree_projects), list)

        for index in range(2):
            project = list_of_nanodegree_projects[index]
            actual_title = project['title']
            expected_title = list_of_projects[index]['title']

            self.assertEqual(expected_title, actual_title)
            self.assertTrue('id' in project)
            self.assertTrue('nanodegree_id' in project)
            self.assertEqual(type(project['id']), int)
            self.assertEqual(type(project['nanodegree_id']), int)
            self.assertEqual(project['nanodegree_id'], nanodegree_id)

    def test_400_error_create_nanodegree_projects(self):
        """
        A request to create a nanodegree project should return a 400 error if the request payload is not properly formatted
        """

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # create projects for this nanodegree
        list_of_projects = list_of_projects = [
            {"title": "Fyyur: Events booking portal", "id": "DROP TABLE projects;"},
            {"Title": 1234}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 400)

    def test_401_error_create_nanodegree_projects(self):
        """
        A request to create a nanodegree by an invalid user should return a 401 status code
        """

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # create projects for this nanodegree
        list_of_projects = list_of_projects = [
            {"title": "Fyyur: Events booking portal"},
            {"title": "Coffee Shop Fullstack"}
        ]

        response_object = self.create_project_request(
            auth_token=self.invalid_random_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 401)

    def test_403_error_create_nanodegree_projects(self):
        """
        A request to create a nanodegree by an authenticated user who is not an admin should return a 403 status code
        """

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"},
            {"title": "Coffee Shop Fullstack"}
        ]

        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        response_object = self.create_project_request(
            auth_token=student_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 403)

    def test_200_success_and_409_conflict_enroll_in_nanodegree(self):
        """
        A request to enroll in a nanodegree by an authenticated user should return a 200 status code.

        Subsequent requests to re-enroll in that same Nanodegree should return a 409 conflict error.
        """
        # create a nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)

        response_object = self.client().get(endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 409)

    def test_200_success_get_nanodegree_students(self):
        """
        A request by an admin to get a list of students enrolled in a Nanodegree should be successful
        """

        # create a nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Enroll student in the nanodegree
        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)

        # Enroll admin in the nanodegree
        headers = {
            "Authorization": f"Bearer {admin_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)

        # get list of students enrolled in Nanodegree
        students_list_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/students"

        headers = {
            "Authorization": f"Bearer {admin_token}"
        }

        response_object = self.client().get(students_list_endpoint, headers=headers)

        response_body = response_object.get_json()

        data = response_body['data']

        # Ensure that the data is returned in the right shape
        self.assertEqual(response_object.status_code, 200)
        self.assertTrue("nanodegree" in data)
        self.assertTrue("students" in data)
        self.assertTrue("total_number_of_students" in data)
        self.assertTrue("has_next_page" in data)
        self.assertTrue("next_page" in data)
        self.assertTrue("has_previous_page" in data)
        self.assertTrue("previous_page" in data)

        # Ensure that the data returned is of the right type and within the expected ranges
        self.assertTrue(type(data['nanodegree']), str)
        self.assertTrue(type(data['students']), list)

        for student in data['students']:
            self.assertEqual(type(student), dict)
            self.assertTrue("id" in student)

        self.assertTrue(type(data['total_number_of_students']), int)
        self.assertTrue(type(data['has_next_page']), bool)
        self.assertTrue(data['next_page'] is None or data['next_page'] >= 2)
        self.assertTrue(type(data['has_previous_page']), bool)
        self.assertTrue(data['previous_page']
                        is None or data['previous_page'] >= 1)


class QuestionsTestCase(TestSetup):
    """Test cases to ensure that CRUD operations on the Question model work as expected"""

    invalid_random_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    def get_auth_token_from_Auth0(self, client_id=None, client_secret=None):
        """
        This returns an auth0 token for the provided login credentials
        """

        AUTH0_TENANT_DOMAIN = os.getenv('AUTH0_TENANT_DOMAIN')

        url = f'https://{AUTH0_TENANT_DOMAIN}/oauth/token'

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": os.getenv('AUTH0_API_AUDIENCE'),
            "grant_type": "client_credentials"
        }

        response_object = requests.post(url=url, json=payload)

        response_data = response_object.json()

        if "access_token" in response_data and "token_type" in response_data:
            return response_data['access_token']

        return None

    def create_nanodegree_request(self, auth_token=None, nanodegree_details={}):
        """
        Helper method for creating nanodegrees

        Returns the http response object
        """

        endpoint = "api/v1/nanodegrees"

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response_object = self.client().post(
            endpoint, headers=headers, json=nanodegree_details)

        return response_object

    def create_project_request(self, auth_token=None, nanodegree_id=None, list_of_projects=[]):
        """
        Helper method for creating nanodegree projects

        Returns the http response object
        """
        endpoint = f"api/v1/nanodegrees/{nanodegree_id}/projects"

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        payload = {"projects": list_of_projects}

        response_object = self.client().post(
            endpoint, headers=headers, json=payload)

        return response_object

    def test_201_success_post_question(self):
        """
        A request to create a question should return a 201 success status if the required data is provided in the right format.
        """
        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        question_data = response_object.get_json()['data']

        # Tests to ensure that the API returns the right shape
        self.assertTrue('id' in question_data)
        self.assertTrue('title' in question_data)
        self.assertTrue('asked_by' in question_data)
        self.assertTrue('nanodegree_id' in question_data)
        self.assertTrue('project_id' in question_data)

        # Assertions to ensure that the appropriate data types are returned

        self.assertTrue(type(question_data['title']) is str)
        self.assertTrue(type(question_data['asked_by']) is int)
        self.assertTrue(type(question_data['nanodegree_id']) is int)
        self.assertTrue(type(question_data['project_id']) is int)

    def test_400_error_post_question(self):
        """
        A request to create a new question should return a 400 error if the input data is incomplete and/or provided in the wrong format
        """

        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        payloads = [3, 'question', {}, {'title': "Is this a title?",
                                        'details': {}, 'asked_by': 8989898, 'project_id': 309}, (), []]

        for payload in payloads:
            response_object = self.client().post(endpoint, headers=headers, json=payload)

            self.assertEqual(response_object.status_code, 400)

    def test_200_success_get_paginated_questions(self):
        """
        A request to get all questions should successfully return the questions in the right format
        """

        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create questions

        endpoint = 'api/v1/questions'

        list_of_payloads = [{
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }, {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }, {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }]

        for payload in list_of_payloads:
            response_object = self.client().post(endpoint, headers=headers, json=payload)
            self.assertEqual(response_object.status_code, 201)

        endpoint = 'api/v1/questions'

        response_object = self.client().get(endpoint)

        self.assertEqual(response_object.status_code, 200)

        response_data = response_object.get_json()['data']

        self.assertTrue("questions" in response_data)
        self.assertTrue("total_number_of_questions" in response_data)
        self.assertTrue("has_next_page" in response_data)
        self.assertTrue("has_previous_page" in response_data)
        self.assertTrue("next_page" in response_data)
        self.assertTrue("previous_page" in response_data)

        list_of_questions = response_data['questions']

        for question_data in list_of_questions:
            # Assertions to ensure that the API returns the right shape for the question data
            self.assertTrue('id' in question_data)
            self.assertTrue('title' in question_data)
            self.assertTrue('asked_by' in question_data)
            self.assertTrue('nanodegree_id' in question_data)
            self.assertTrue('project_id' in question_data)

            # Assertions to ensure that the appropriate data types are returned

            self.assertTrue(type(question_data['title']) is str)
            self.assertTrue(type(question_data['asked_by']) is int)
            self.assertTrue(type(question_data['nanodegree_id']) is int)
            self.assertTrue(type(question_data['project_id']) is int)

    def test_200_success_patch_question(self):
        """
        A request to update a question should be successful if the required input data is provided in the right format
        """
        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        # Step 5: Update question

        # Get question ID
        question_id = response_object.get_json()['data']['id']

        # Make a patch request
        endpoint = f'api/v1/questions/{question_id}'

        updated_question_data = {
            'title': "Updated question data?",
            'details': "Please help!!!!",
            'github_link': "https://github.com/dev-nebe"
        }

        response_object = self.client().patch(
            endpoint, headers=headers, json=updated_question_data)

        self.assertEqual(response_object.status_code, 200)

        response_body = response_object.get_json()

        updated_title = response_body['data']['title']

        self.assertEqual(updated_question_data['title'], updated_title)

    def test_400_error_patch_question(self):
        """
        A request to update a question should return a 400 error if the required input data is in the wrong format
        """
        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        # Step 5: Update question

        # Get question ID
        question_id = response_object.get_json()['data']['id']

        # Make a patch request
        endpoint = f'api/v1/questions/{question_id}'

        updated_question_data = {
            'title': 3,
            'details': {},
        }

        response_object = self.client().patch(
            endpoint, headers=headers, json=updated_question_data)

        self.assertEqual(response_object.status_code, 400)

    def test_403_error_patch_question(self):
        "A request to patch a question which was not posted by the person making the request should return a 403 error"

        """
        A request to update a question should be successful if the required input data is provided in the right format
        """
        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        # Step 5: Update question

        # Get question ID
        question_id = response_object.get_json()['data']['id']

        # Make a patch request
        endpoint = f'api/v1/questions/{question_id}'

        headers = headers = {
            "Authorization": f"Bearer {admin_token}"
        }

        updated_question_data = {
            'title': "Updated question data?",
            'details': "Please help!!!!",
            'github_link': "https://github.com/dev-nebe"
        }

        response_object = self.client().patch(
            endpoint, headers=headers, json=updated_question_data)

        self.assertEqual(response_object.status_code, 403)

    def test_200_success_delete_question(self):
        """
        A request to delete a question should be successful if the user has sufficient authorization i.e, the user is the owner of the question
        """

        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        # Step 5: Delete question

        # Get question ID
        question_id = response_object.get_json()['data']['id']

        # Make a delete request
        endpoint = f'api/v1/questions/{question_id}'

        response_object = self.client().delete(
            endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)

    def test_403_error_delete_question(self):
        """
        A request to delete a question should return a 403 error if the user isn't the owner of the question
        """

        # Step 1: create nanodegree
        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=admin_token, nanodegree_details=nanodegree_details)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['id']

        # Step 2: Create projects for this nanodegree
        list_of_projects = [
            {"title": "Fyyur: Events booking portal"}
        ]

        response_object = self.create_project_request(
            auth_token=admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created project
        response_body = response_object.get_json()

        # project_id = response_body['data']['id']

        project_id = 1

        # self.assertTrue(type(project_id) is int)

        # Step 3: Enroll student in Nanodegree
        enrollment_endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/enroll"

        # Get student token
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        headers = {
            "Authorization": f"Bearer {student_token}"
        }

        response_object = self.client().get(enrollment_endpoint, headers=headers)

        self.assertEqual(response_object.status_code, 200)
        # enrollment successfull

        # Step 4: Create question

        endpoint = 'api/v1/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'nanodegree_id': nanodegree_id,
            'project_id': project_id,
            'github_link': None
        }

        response_object = self.client().post(endpoint, headers=headers, json=payload)

        self.assertEqual(response_object.status_code, 201)

        # Step 5: Delete question

        # Get question ID
        question_id = response_object.get_json()['data']['id']

        # Make a delete request
        endpoint = f'api/v1/questions/{question_id}'

        response_object = self.client().delete(
            endpoint, headers={
                "Authorization": f"Bearer {admin_token}"
            })

        self.assertEqual(response_object.status_code, 403)
