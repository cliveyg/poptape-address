import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    # set app configs
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHECK_ACCESS_URL = os.getenv('CHECK_ACCESS_URL')

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TESTDB_URI')
