import os
import random
import json
import sqlalchemy
from src.tests.base import TestSetup
from src.app.models.user import User
from src.app.models.nanodegree import Nanodegree
from src.app.models.project import Project
from src.app.models.question import Question
from src.app.models.answer import Answer


class UserModelTestCases(TestSetup):
    """
    Tests to ensure that CRUD operations on the user model work as expected
    """

    def test_successful_user_creation(self):
        """Test successful creation of user"""

        user1 = User(jwt_subject="loakjdpao33434")
        user2 = User(jwt_subject="akld408404klaefja")

        user1.save()
        user2.save()

        list_of_users = User.query.all()

        self.assertEqual(type(list_of_users), list)
        self.assertEqual(len(list_of_users), 2)

    def test_unique_constraint_error_user_creation(self):
        """Ensure that an integrity error is raised when the same user is inserted twice into the db"""
        try:
            user1 = User(jwt_subject="akld408404klaefja")
            user1.save()

            user2 = User(jwt_subject="akld408404klaefja")
            user2.save()

        except sqlalchemy.exc.IntegrityError:
            self.assertTrue(True)


class NanodegreeModelTestCases(TestSetup):
    """
    Tests to ensure that CRUD operations on the nanodegree model work as expected
    """

    def test_successful_nanodegree_creation(self):
        """Test successful creation of nanodegree"""

        FSND = Nanodegree(title="Full Stack Developer Nanodegree",
                          description="None for now")

        FSND.save()

        DEND = Nanodegree(title="Data Engineer Nanodegree",
                          description="None for now")

        DEND.save()

        list_of_nanodegrees = Nanodegree.query.all()

        self.assertEqual(type(list_of_nanodegrees), list)
        self.assertEqual(len(list_of_nanodegrees), 2)


class ProjectModelTestCases(TestSetup):
    """
    Tests to ensure that CRUD operations on the project model work as expected
    """

    def test_successful_project_creation(self):
        """Test successful creation of project"""

        try:
            FSND = Nanodegree(
                title="Full Stack Developer Nanodegree", description="None for now")

            fyyur = Project(title="Fyyur: Events booking site")

            coffee_shop = Project(title="Coffee Shop Fullstack")

            FSND.projects.append(fyyur)
            FSND.projects.append(coffee_shop)

            FSND.save()
            fyyur.save()
            coffee_shop.save()

            list_of_projects = Project.query.all()

            self.assertEqual(type(list_of_projects), list)
            self.assertTrue(len(list_of_projects), 3)

            for project in list_of_projects:

                self.assertEqual(project.nanodegree.title,
                                 "Full Stack Developer Nanodegree")

        except:
            self.assertTrue(False)


class Question_And_Answer_Models_Test_Cases(TestSetup):
    """
    Tests to ensure that CRUD operations on the question and answer models work as expected
    """

    def test_successful_question_creation(self):
        """Test successful creation of question and answer"""

        user1 = User(jwt_subject="loakjdpao33434")

        FSND = Nanodegree(title="Full Stack Developer Nanodegree",
                          description="None for now")

        fyyur = Project(title="Fyyur: Events booking site")

        question_one = Question(
            title="Hi, is there an easier way to do this?", details="None for now")

        answer_one = Answer(
            details="Tbh, I don't know. We'll have to check online")

        question_one.answers.append(answer_one)
        user1.answers.append(answer_one)
        user1.questions.append(question_one)
        fyyur.questions.append(question_one)
        FSND.projects.append(fyyur)
        FSND.questions.append(question_one)

        question_one.save()
        user1.save()
        fyyur.save()
        FSND.save()

        self.assertEqual(question_one.id, 1)
        self.assertEqual(answer_one.id, 1)
        self.assertEqual(fyyur.id, 1)
        self.assertEqual(FSND.id, 1)

        self.assertEqual(question_one.nanodegree_id, 1)
        self.assertEqual(question_one.project_id, 1)
        self.assertEqual(len(question_one.answers), 1)
        self.assertEqual(answer_one.question_id, 1)
