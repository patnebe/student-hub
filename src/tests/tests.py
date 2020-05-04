from src.app.models.user import User
from src.tests.base import TestSetup
import os
import random
import json


class QuestionsTestCase(TestSetup):
    def test_201_success_post_question(self):
        """
        A request to create a question should be successful if the required data is provided in the right format.
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

        payloads = [3, 'question', {}, {'title': "Is this a title?", 'details': "More details", 'asked_by': 8989898, 'project_id': 309}, (), []]

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



class AnswersTestCase(TestSetup):
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