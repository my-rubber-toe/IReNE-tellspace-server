"""
Configuration File: config.py
=============================
Author: Roberto Guzmán <roberto.guzman3@upr.edu>

Holds the configuration options to be used as environment variables.
"""

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

FLASK_APP = os.getenv("FLASK_APP") # The app source file to use upon server creation.
FLASK_ENV = os.getenv("FLASK_ENV") # The environment in whicht the application runs. (i.e:)
PORT = os.getenv("PORT")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv("DB_HOST")

# Authorization
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_SALT = os.getenv("FLASK_SALT")