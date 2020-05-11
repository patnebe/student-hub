from src.app.models.user import User
from src.tests.base import APITestSetup
import os
import random
import json
import requests
import pytest


class NanodegreeTestCase(APITestSetup):
    """"""

    admin_token = None
    student_token = None
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
        token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        # set token as a class property so subsequent tests won't need to request new tokens
        self.admin_token = token

        # Utilize the auth0 token to create a nanodegree
        payload = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=payload)

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
        """"""
        # Retreive login credentials
        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        # Get auth token with sufficient authorization (Admin role) from auth0 endpoint
        token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        # set token as a class property so subsequent tests won't need to request new tokens
        self.admin_token = token

        # Utilize the auth0 token to create a nanodegree
        list_of_payloads = [{
            "description": "None for now"
        }, {}, 1, "invalid string payload", []]

        for payload in list_of_payloads:
            response_object = self.create_nanodegree_request(
                auth_token=self.admin_token, nanodegree_details=payload)

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
        """ """
        """
        A request to create a nanodegree by an authenticated user who is not an admin should return a 403 status code
        """

        # Retreive login credentials
        student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
        student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')

        # Get auth token with insufficient authorization (student role) from auth0 endpoint
        token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        self.student_token = token

        # Utilize the auth0 token to create a nanodegree
        payload = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=self.student_token, nanodegree_details=payload)

        self.assertEqual(response_object.status_code, 403)

    def test_200_success_get_nanodegrees(self):
        """
        A GET request to /nanodegrees should return a list of all the available nanodegrees
        """

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        if self.admin_token is None:
            token = self.get_auth_token_from_Auth0(
                client_id=admin_client_id, client_secret=admin_client_secret)

            self.admin_token = token

        payload_one = {
            "title": "Full Stack Developer Nanodegree",
            "description": "None for now"
        }

        payload_two = {
            "title": "Data Engineer Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=payload_one)

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=payload_two)

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

        if self.admin_token is None:
            token = self.get_auth_token_from_Auth0(
                client_id=admin_client_id, client_secret=admin_client_secret)

            self.admin_token = token

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=nanodegree_details)

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
            auth_token=self.admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

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
        """"""

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        if self.admin_token is None:
            token = self.get_auth_token_from_Auth0(
                client_id=admin_client_id, client_secret=admin_client_secret)

            self.admin_token = token

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=nanodegree_details)

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
            auth_token=self.admin_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 400)

    def test_401_error_create_nanodegree_projects(self):
        """"""

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        self.admin_token = token

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=nanodegree_details)

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
        """

        nanodegree_details = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
        admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

        self.admin_token = self.get_auth_token_from_Auth0(
            client_id=admin_client_id, client_secret=admin_client_secret)

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=nanodegree_details)

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

        self.student_token = self.get_auth_token_from_Auth0(
            client_id=student_client_id, client_secret=student_client_secret)

        response_object = self.create_project_request(
            auth_token=self.student_token, nanodegree_id=nanodegree_id, list_of_projects=list_of_projects)

        self.assertEqual(response_object.status_code, 403)

    # def test_200_success_get_nanodegree_students(self):
    #     """
    #     """

    #     nanodegree_details = {
    #         "title": "Test Nanodegree",
    #         "description": "None for now"
    #     }

    #     response_object = self.create_nanodegree_request(
    #         auth_token=self.admin_token, nanodegree_details=nanodegree_details)

    #     self.assertEqual(response_object.status_code, 201)

    #     # get the id of the created nanodegree
    #     response_body = response_object.get_json()

    #     nanodegree_id = response_body['data']['nanodegree_id']

    #     endpoint = f"/api/v1/nanodegrees/{nanodegree_id}/students"

    #     ###############################
    #     ###############################
    #     ##### Post some students ######
    #     ###############################
    #     ###############################

    #     response_object = self.client().get(endpoint)

    #     response_body = response_object.get_json()

    #     self.assertEqual(response_object.status_code, 200)


# class QuestionsTestCase(APITestSetup):
#     def test_201_success_post_question(self):
#         """
#         A request to create a question should return a 201 success status if the required data is provided in the right format.
#         """

#         endpoint = 'api/v1/questions'

#         payload = {
#             'title': "Hi, my tests are passing. How do I stop this?",
#             'details': "Please help!!!!",
#             'asked_by': 8989898,
#             'nanodegree_id': 44,
#             'project_id': 309,
#             'github_link': None
#         }

#         response_object = self.client().post(endpoint, json=payload)

#         self.assertEqual(response_object.status_code, 201)

#     def test_400_error_post_question(self):
#         """
#         A request to create a new question should return a 400 error if the input data is incomplete and/or provided in the wrong format
#         """
#         endpoint = 'api/v1/questions'

#         payloads = [3, 'question', {}, {'title': "Is this a title?",
#                                         'details': "More details", 'asked_by': 8989898, 'project_id': 309}, (), []]

#         for payload in payloads:
#             response_object = self.client().post(endpoint, json=payload)

#             self.assertEqual(response_object.status_code, 400)

#     def test_200_success_get_questions(self):
#         """
#         A request to get all questions should successfully return the questions in the right format
#         """
#         endpoint = 'api/v1/questions'

#         response_object = self.client().get(endpoint)

#         self.assertEqual(response_object.status_code, 200)

#     def test_success_patch_question(self):
#         """
#         A request to update a question should be successful if the required input data is provided in the right format
#         """
#         pass

#     def test_201_success_post_question_comment(self):
#         """
#         A request to post a comment on a question should be successful if the required input data is provided in the right format
#         """
#         pass

#     def test_200_success_delete_question_comment(self):
#         """
#         A request to delete a comment posted on a question should be successful
#         """
#         pass

#     def test_404_success_delete_question_comment(self):
#         """
#         A request to delete a non-existent/previously deleted comment on a question should return a 404 error
#         """

#     def test_200_success_create_question_vote(self):
#         """
#         A request to upvote or downvote a question should be successful
#         """
#         pass

#     def test_200_success_edit_question_vote(self):
#         """
#         A request to edit a vote should be successful
#         """
#         pass

#     def test_200_success_delete_question_vote(self):
#         """
#         A request to delete a vote should be successful
#         """
#         pass


# class AnswersTestCase(APITestSetup):

#     def test_success_post_answer(self):
#         pass

#     def test_success_post_answer_comment(self):
#         pass

#     def test_success_get_answers(self):
#         pass

#     def test_success_patch_answer(self):
#         pass

#     def test_success_patch_question_comment(self):
#         pass

#     def test_success_patch_answer_comment(self):
#         pass

#     def test_success_delete_answer_comment(self):
#         pass

#     def test_success_toggle_answer_acceptance(self):
#         pass

#     def test_success_create_answer_vote(self):
#         pass

#     def test_success_edit_answer_vote(self):
#         pass

#     def test_success_delete_answer_vote(self):
#         pass
