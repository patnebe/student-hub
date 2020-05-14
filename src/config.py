import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
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

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_CONNECT_OPTIONS = {}

    DEBUG = True

    STUDENTS_PER_PAGE = 10

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY') or "secret"

    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or "this-should-be-a-secret"


class TestConfig(DevelopmentConfig):
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


# Remember to setup a deployment config class
