from os import path, getenv
from datetime import timedelta

from dotenv import load_dotenv

# load dotenv in the base root
basedir = path.join(path.dirname(__file__))
dotenv_path = path.join(basedir, '.env')
load_dotenv(dotenv_path)
db_path = path.join(path.dirname(__name__), '../company.db')
DEFAULT_DB_URL = "sqlite:///{}".format(db_path)
# DEFAULT_DB_URL = "postgresql://oooo:dodo@localhost:5432/oooo"
# DEFAULT_TEST_DB_URL = "postgresql://oooo:dodo@localhost:5432/oooo"
db_test_path = path.join(path.dirname(__name__), '../company_test.db')
DEFAULT_TEST_DB_URL = "sqlite:///{}".format(db_test_path)


class Config(object):
    """Parent Babe configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = getenv('SECRET', 'dodo@N9shiv:)()')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', DEFAULT_DB_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_URL_RULE = '/api/v1/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = timedelta(hours=24)


class DevelopmentConfig(Config):
    """Configuration for Development"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Configuration for Testing"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DEFAULT_TEST_DB_URL', DEFAULT_TEST_DB_URL)
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
