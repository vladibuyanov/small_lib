""" Configuration file """
import os

SECRET_KEY = os.getenv('KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///small-lib.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
