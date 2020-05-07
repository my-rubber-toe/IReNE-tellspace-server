"""
authentication.py
====================================
Blueprint class that holds the endpoints that perform authentication operations. These endpoints are responsible for
the generation, refreshing and revoking of access tokens.
"""

from flask import current_app, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, \
    jwt_required, get_jwt_identity, get_raw_jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from utils.responses import ApiResult
from utils.exceptions import TellSpaceAuthError

from cachetools import TTLCache

from datetime import timedelta

from TS_DAOs.dao_TS import *
from TS_DAOs.schema_DB import *

bp = Blueprint('authentication', __name__, url_prefix='/auth')

# Set tll to the same time of the ttl of the token #
blacklist = TTLCache(maxsize=10000, ttl=120)


@bp.route("/login/<google_token>", methods=['GET'])
def get_tokens(google_token: str):
    """
        Verify if the given param string is a valid Google idToken issued by Google and made with the projects
        credentials. If the user is NOT banned and is approved, proceed with token generation.

        Parameters
        ----------
            google_token
                the JWT Google generated token to be evaluated.

        Returns
        -------
            ApiResult
                the response object containing a JSON Object with two tokens: access_token and refresh_token,
            respectively.

            TellSpaceAuthError
                Exception Class.

    """
    id_info = id_token.verify_oauth2_token(
        google_token,
        requests.Request(),
        current_app.config['GOOGLE_OAUTH_CLIENT_ID'])

    # Verify that the token was indeed issued by google accounts.
    if id_info['iss'] != 'accounts.google.com':
        raise TellSpaceAuthError(msg="Wrong issuer. Token issuer is not Google.")

    collab: Collaborator = get_me(id_info['email'])

    if (not collab.banned) and collab.approved:
        access_token_ttl = 5
        refresh_token_ttl = 10

        return ApiResult(
            # access_token=create_access_token(identity=id_info['email'], expires_delta=timedelta(hours=30),
            access_token=create_access_token(identity=collab.email, expires_delta=timedelta(hours=access_token_ttl)),
            refresh_token=create_refresh_token(identity=collab.email, expires_delta=timedelta(hours=refresh_token_ttl)),
            access_token_ttl=access_token_ttl,
            refresh_token_ttl=refresh_token_ttl
        )

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )


@bp.route('/me', methods=['GET'])
@jwt_required
def auth_me():
    """"
        Get the collaborator information from the database. (First Name, Last Name, Email and id)

        Returns
        -------
            ApiResult
                the response object containing a JSON Object with the collaborators first name, last name, email
                and id.

            TellSpaceAuthError
                Exception class for authentication errors.

    """
    email = get_jwt_identity()

    collab: Collaborator = get_me(email)

    if (not collab.banned) and collab.approved:
        return ApiResult(
            first_name=collab.first_name,
            last_name=collab.last_name,
            email=collab.email
        )

    raise TellSpaceAuthError(
        msg='Authorization Error. Collaborator is banned or has not been approved by the admin.',
        status=401
    )


@bp.route('/refresh', methods=["GET"])
@jwt_refresh_token_required
def auth_refresh():
    """
        Return a new access_token given a valid refresh token.

        Returns
        -------
            ApiResult
                the response object containing a JSON Object with the new access_token

            TellSpaceAuthError
                Exception class for authentication errors.
    """
    email = get_jwt_identity()
    access_token = create_access_token(identity=email, expires_delta=timedelta(hours=2))
    return ApiResult(access_token=access_token)


@bp.route("/logout", methods=["DELETE"])
@jwt_required
def auth_logout():
    """
        Revoke access token. Add access tokens to blacklist.

        Returns
        -------
            ApiResult
                the response object containing a JSON Object with acknowledgment message.

            TellSpaceAuthError
                Exception class for authentication errors.
    """
    jti = get_raw_jwt()['jti']
    blacklist[jti] = True
    return ApiResult(message="Successfully logged out.")


@current_app.jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
        Verifies if a token has been blacklisted. Token exists within the blacklist cache.

        Parameters
        ----------
            decrypted_token
                the token string to be evaluated.

        Returns
        -------
            entry
                the key of the blacklist set which points to the blacklisted token.

            False
                boolean value if a token is not found in the blacklist.
    """
    jti = decrypted_token['jti']
    if blacklist.currsize == 0:
        return False
    entry = blacklist.get(jti)
    return entry
