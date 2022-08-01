from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'flask_api/static/uploads'
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./database/library.db'
    DEBUG = True


class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./dev_database/dev_library.db'
