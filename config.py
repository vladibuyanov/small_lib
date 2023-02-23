""" Configuration file """
import os

SECRET_KEY = os.getenv('KEY', 'something_really_secret')
DEBUG = os.getenv('DEBUG', True)

SQLALCHEMY_DATABASE_URI = 'sqlite:///small-lib.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
