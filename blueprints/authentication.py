# TODO: Implement authentication strategy with flask dance and Google oAuth. Use decorators as needed.


from flask import redirect, url_for, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils.responses import ApiResult, ApiException
from utils.exceptions import TellSpaceAuthError

# Register Google oAuth Strategy blueprint
bp = make_google_blueprint(scope=["profile", "email"])
bp.url_prefix = "/"


@bp.route('/')
def auth_main():
    """Generate a new access token for the user.
        User must perform Google oAuth sign in to get a valid token.
    """
    if not google.authorized:
        raise TellSpaceAuthError(msg="Client is not unauthorized. Please login at /google")

    # Get credentials from Google
    email = google.get("/oauth2/v2/userinfo").json()['email']

    # TODO: Check if user email exists in DB as an approved collaborator.

    access_token = create_access_token(identity=email)
    return ApiResult(access_token=access_token)


@bp.route('/me', methods=["GET"])
@jwt_required
def auth_me():
    # TODO: Check if user has a valid token. Returns the token identity.
    return ApiResult(identity=get_jwt_identity())


@bp.route("/logout")
def auth_logout():
    try:
        token = bp.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        del bp.token
    except KeyError:
        raise TellSpaceAuthError(msg="No token to be revoked. Please login at /api/auth/login")

    return jsonify(response="Token successfully revoked!")


