from flask import current_app, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, \
    jwt_required, get_jwt_identity, get_raw_jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from utils.responses import ApiResult, ApiException
from utils.exceptions import TellSpaceAuthError

from cachetools import TTLCache

from datetime import timedelta

from daos.dao_TS import *
from database.schema_DB import *

bp = Blueprint('authentication', __name__, url_prefix='/auth')

# Set blacklist set for blacklisted tokens
# TODO: Replace blacklist with a Redis Store
# Set tll to the same time of the ttl of the token #
blacklist = TTLCache(maxsize=10000, ttl=120)


@current_app.jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Verifies if a token has been blacklisted."""
    jti = decrypted_token['jti']
    if blacklist.currsize == 0:
        return False
    entry = blacklist.get(jti)  #search for the jti on the blacklist#
    return entry

@bp.route("/login/<google_token>", methods=['GET'])
def get_tokens(google_token: str):
    """Verify if the given param string is a valid Google idToken. Return 2 tokens to be used as the authentication.
    """
    id_info = id_token.verify_oauth2_token(
        google_token,
        requests.Request(),
        current_app.config['GOOGLE_OAUTH_CLIENT_ID'])

    # Verify that the token was indeed issued by google accounts.
    if id_info['iss'] != 'accounts.google.com':
        raise TellSpaceAuthError(msg="Wrong issuer. Token issuer is not Google.")

    collab: Collaborator = get_me(id_info['email'])
    if not collab.banned:
        return ApiResult(
            # access_token=create_access_token(identity=id_info['email'], expires_delta=timedelta(hours=30),
            access_token=create_access_token(identity= collab.email, expires_delta=timedelta(days=30)),
            refresh_token=create_refresh_token(identity=collab.email, expires_delta=timedelta(days=30))
        )



@bp.route('/me', methods=['GET'])
@jwt_required
def auth_me():
    """"Return the user information from the database."""
    # Use DAOs to look for user in the database.
    email = get_jwt_identity()
    collab : Collaborator = get_me(email)


    if (not collab.banned) and collab.approved:
        return ApiResult(
            id=collab.id.__str__(),
            first_name=collab.first_name,
            last_name=collab.email,
            email=collab.email
        )

    raise TellSpaceAuthError(msg="Access denied. User is not approved or is banned.")


@bp.route('/refresh', methods=["GET"])
@jwt_refresh_token_required
def auth_refresh():
    """Return a new access_token given a valid refresh token."""
    email = get_jwt_identity()
    access_token = create_access_token(identity=email, expires_delta=timedelta(hours=2))
    return ApiResult(access_token=access_token)


@bp.route("/logout")
@jwt_required
def auth_logout():
    """Revoke the Google authorization and add tokens to blacklist"""
    jti = get_raw_jwt()['jti']
    blacklist[jti] = True   # Add the jti to the cache with value true #
    return ApiResult(message="Successfully logged out.")