from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
PORT = os.getenv("PORT")

FLASK_DEBUG = os.getenv("FLASK_DEBUG")
DB_HOST = os.getenv("DB_HOST")


# Authorization
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_SALT = os.getenv("FLASK_SALT")
