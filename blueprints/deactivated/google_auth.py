# TODO: Implement authentication strategy with flask dance and Google oAuth. Use decorators as needed.

from flask_dance.contrib.google import make_google_blueprint, google

from utils.exceptions import TellSpaceAuthError


# Register Google oAuth Strategy blueprint
bp = make_google_blueprint(scope=["profile", "email"])
bp.url_prefix = "/"

@bp.route('/', methods=['GET'])
def auth_main():
    """Generate a new access token for the user. Client must sign in to Google oAuth to get a valid token.
        Client must be approved and NOT banned.
    """
    if not google.authorized:
        raise TellSpaceAuthError(msg="Client is not unauthorized. Please login at /google", status=401)

    # Get user email from Google Credentials to use as identity
    user = google.get("/oauth2/v2/userinfo").json()

    return bp.token['access_token']




