# TODO: Implement authentication strategy with flask dance and Google oAuth. Use decorators as needed.


from flask import redirect, url_for, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from utils.responses import ApiResult, ApiException
from utils.exceptions import TellSpaceAuthError

# Register Google oAuth Strategy blueprint
bp = make_google_blueprint(scope=["profile", "email"])
bp.url_prefix = "/"


@bp.route('/')
def auth_main():
    # TODO: Check if user has a valid session token. Use decorator function.
    if not google.authorized:
        raise TellSpaceAuthError(msg="Client is not unauthorized. Please login at /api/auth/login")

    return ApiResult(message="Client Authorized")


@bp.route('/api/auth/me', methods=["GET"])
def auth_me():

    # TODO: Check if user has a valid session token. Returns the relevant user information from database.
    if not google.authorized:
        raise TellSpaceAuthError(msg="Client is not unauthorized. Please login at /api/auth/login")

    resp = google.get("/oauth2/v2/userinfo").json()

    return ApiResult(
        value={
            "response": resp
        }
    )


@bp.route('/api/auth/login', methods=["GET"])
def auth_login():

    # TODO: If valid token exists return ApiException

    if not google.authorized:
        return redirect(url_for("google.login"))

    # TODO: Create new token and return it to the client

    return ApiResult(
        value={
            "response": "Client authorized."
        }
    )


@bp.route("/api/auth/logout")
def auth_logout():
    try:
        token = bp.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(resp)
        del bp.token
    except KeyError:
        return jsonify(response="No token to be revoked. Please login at /api/auth/login")

    return jsonify(response="Token successfully revoked!")


