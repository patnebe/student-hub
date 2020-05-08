from src.app.models.user import User
from src.tests.base import APITestSetup
import os
import random
import json


class NanodegreeTestCase(APITestSetup):
    """"""

    admin_token = None
    student_token = None
    invalid_random_token = "8024j0029fjlskdpoiajclif"

    def get_auth_token_from_Auth0(self, email_or_username, password):
        """
        This returns an auth0 token for the provided login credentials
        """

        return

    def create_nanodegree_request(self, auth_token=None, nanodegree_details={}):
        """
        Helper method for creating nanodegrees

        Returns the http response object
        """

        endpoint = "api/v1/nanodegrees"

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response_object = self.client.post(
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

        create_projects_response = self.client.post(
            endpoint, headers=headers, json=payload)

        return create_projects_response

    def test_201_success_create_nanodegree(self):
        """
        A request by an admin to create a nanodegree should return a 201 status code
        """

        # Retreive login credentials
        admin_email = os.getenv('STUDENT_HUB_ADMIN')
        admin_password = os.getenv('STUDENT_HUB_ADMIN_PASSWORD')

        # Get auth token with sufficient authorization (Admin role) from auth0 endpoint
        token = self.get_auth_token_from_Auth0(
            email_or_username=admin_email, password=admin_password)

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

        self.assertEqual(response_object.status_code, 201)
        self.assertEqual(type(response_body.nanodegree), dict)
        # response_body.nanodegree should have the following schema {title: string, description: string}

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
        student_email = os.getenv('STUDENT_HUB_STUDENT_EMAIL')
        student_password = os.getenv('STUDENT_HUB_STUDENT_PASSWORD')

        # Get auth token with insufficient authorization (student role) from auth0 endpoint
        token = self.get_auth_token_from_Auth0(
            email_or_username=student_email, password=student_password)

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

        endpoint = 'api/v1/nanodegrees'

        response_object = self.client().get(endpoint)
        response_body = response_object.get_json()

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(type(response_body.data), list)

        list_of_nanodegrees = response_body.data

        if len(list_of_nanodegrees) > 0:
            for nanodegree in list_of_nanodegrees:
                # add a line of code to validate the content of each nanodegree object
                pass

    def test_201_success_create_nanodegree_projects(self):
        """
        A POST request to /nanodegree/<int:id>/projects should return a 201 success and all the projects for the specified nanodegree
        """

        # create a nanodegree
        payload = {
            "title": "Test Nanodegree",
            "description": "None for now"
        }

        response_object = self.create_nanodegree_request(
            auth_token=self.admin_token, nanodegree_details=payload)

        self.assertEqual(response_object.status_code, 201)

        # get the id of the created nanodegree
        response_body = response_object.get_json()

        nanodegree_id = response_body['data']['nanodegree_id']

        # create projects for this nanodegree
        projects = [
            {},
            {}
        ]

        pass

    def test_401_error_create_nanodegree_projects(self):
        pass

    def test_403_error_create_nanodegree_projects(self):
        pass

    def test_200_success_get_nanodegree_students(self):
        pass


class QuestionsTestCase(APITestSetup):
    def test_201_success_post_question(self):
        """
        A request to create a question should return a 201 success status if the required data is provided in the right format.
        """

        endpoint = '/questions'

        payload = {
            'title': "Hi, my tests are passing. How do I stop this?",
            'details': "Please help!!!!",
            'asked_by': 8989898,
            'nanodegree_id': 44,
            'project_id': 309,
            'github_link': None
        }

        response_object = self.client().post(endpoint, json=payload)

        self.assertEqual(response_object.status_code, 201)

    def test_400_error_post_question(self):
        """
        A request to create a new question should return a 400 error if the input data is incomplete and/or provided in the wrong format
        """
        endpoint = '/questions'

        payloads = [3, 'question', {}, {'title': "Is this a title?",
                                        'details': "More details", 'asked_by': 8989898, 'project_id': 309}, (), []]

        for payload in payloads:
            response_object = self.client().post(endpoint, json=payload)

            self.assertEqual(response_object.status_code, 400)

    def test_200_success_get_questions(self):
        """
        A request to get all questions should successfully return the questions in the right format
        """
        endpoint = '/questions'

        response_object = self.client().get(endpoint)

        self.assertEqual(response_object.status_code, 200)

    def test_success_patch_question(self):
        """
        A request to update a question should be successful if the required input data is provided in the right format
        """
        pass

    def test_201_success_post_question_comment(self):
        """
        A request to post a comment on a question should be successful if the required input data is provided in the right format
        """
        pass

    def test_200_success_delete_question_comment(self):
        """
        A request to delete a comment posted on a question should be successful
        """
        pass

    def test_404_success_delete_question_comment(self):
        """
        A request to delete a non-existent/previously deleted comment on a question should return a 404 error
        """

    def test_200_success_create_question_vote(self):
        """
        A request to upvote or downvote a question should be successful
        """
        pass

    def test_200_success_edit_question_vote(self):
        """
        A request to edit a vote should be successful
        """
        pass

    def test_200_success_delete_question_vote(self):
        """
        A request to delete a vote should be successful
        """
        pass


class AnswersTestCase(APITestSetup):

    def test_success_post_answer(self):
        pass

    def test_success_post_answer_comment(self):
        pass

    def test_success_get_answers(self):
        pass

    def test_success_patch_answer(self):
        pass

    def test_success_patch_question_comment(self):
        pass

    def test_success_patch_answer_comment(self):
        pass

    def test_success_delete_answer_comment(self):
        pass

    def test_success_toggle_answer_acceptance(self):
        pass

    def test_success_create_answer_vote(self):
        pass

    def test_success_edit_answer_vote(self):
        pass

    def test_success_delete_answer_vote(self):
        pass
