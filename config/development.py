from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
PORT = os.getenv("PORT")

FLASK_DEBUG = os.getenv("FLASK_DEBUG")
DB_HOST = os.getenv("DB_HOST")


# Authorization
GOOGLE_OAUTH_CLIENT_ID=""
GOOGLE_OAUTH_CLIENT_SECRET=""
OAUTHLIB_RELAX_TOKEN_SCOPE= True

# Set to TRUE for testing purpouses
OAUTHLIB_INSECURE_TRANSPORT= True
FLASK_SECRET_KEY="SuPeRsEcReTkEyThAtNoOnEcAnCrAcK"
FLASK_SALT="Justasaltysaltthatisverysalty"