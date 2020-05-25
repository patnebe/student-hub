import os
from os.path import dirname, abspath

from dotenv import load_dotenv

basedir = dirname((abspath(__file__)))

load_dotenv(os.path.join(basedir, '.env'))


class DevelopmentConfig(object):
    """
    Flask configuration for development
    """
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    dev_database_name = os.environ.get(
        'DEV_DATABASE_NAME')
    password = os.environ.get(
        'DATABASE_PASSWORD')
    username = os.environ.get(
        'DATABASE_USERNAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@localhost:5432/{dev_database_name}'

    # Modify this and move the heroku postgres database url into the deployment config

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_CONNECT_OPTIONS = {}

    DEBUG = True

    STUDENTS_PER_PAGE = os.environ.get(
        'STUDENTS_PER_PAGE')

    QUESTIONS_PER_PAGE = os.environ.get(
        'QUESTIONS_PER_PAGE')

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2


class TestConfig(object):
    """
    Flask configuration for tests
    """
    TESTING = True

    test_database_name = os.environ.get(
        'TEST_DATABASE_NAME')
    password = os.environ.get(
        'DATABASE_PASSWORD')
    username = os.environ.get(
        'DATABASE_USERNAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@localhost:5432/{test_database_name}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_CONNECT_OPTIONS = {}

    DEBUG = True

    STUDENTS_PER_PAGE = os.environ.get(
        'STUDENTS_PER_PAGE')

    QUESTIONS_PER_PAGE = os.environ.get(
        'QUESTIONS_PER_PAGE')


# Remember to setup a deployment config class
