"""Flask config class."""
from pathlib import Path


class Config(object):
    SECRET_KEY = 'generate_a_secret_key'
    WTF_CSRF_SECRET_KEY = "generate_another_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('data','paralympics_db.sqlite'))
    TESTING = False
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath('static', 'img')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('data', 'paralympics_testdb.sqlite'))
