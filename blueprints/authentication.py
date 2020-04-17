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
import random
import string

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
        return ApiResult(
            # access_token=create_access_token(identity=id_info['email'], expires_delta=timedelta(hours=30),
            access_token=create_access_token(identity=collab.email, expires_delta=timedelta(days=30)),
            refresh_token=create_refresh_token(identity=collab.email, expires_delta=timedelta(days=30))
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin')


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
    # Use DAOs to look for user in the database.
    email = get_jwt_identity()
    collab: Collaborator = get_me(email)

    if (not collab.banned) and collab.approved:
        return ApiResult(
            first_name=collab.first_name,
            last_name=collab.last_name,
            email=collab.email
        )

    raise TellSpaceAuthError(msg='Authorization Error. Collaborator is banned or has not been approved by the admin.')


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


@bp.route("/logout")
@jwt_required
def auth_logout():
    """
        Revoke the Google authorization and add tokens to blacklist.

        Returns
        -------
            ApiResult
                the response object containing a JSON Object with acknowledgment message.

            TellSpaceAuthError
                Exception class for authentication errors.
    """
    jti = get_raw_jwt()['jti']
    blacklist[jti] = True  # Add the jti to the cache with value true #
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
    """
    jti = decrypted_token['jti']
    if blacklist.currsize == 0:
        return False
    # search for the jti on the blacklist#
    entry = blacklist.get(jti)
    return entry


@bp.route("/get-invalid-token")
def get_invalid_token():
    invalid_token = create_access_token(identity='iamnotinthedatabase@email.com', expires_delta=timedelta(days=1))
    invalid_token = invalid_token + ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(1, 10)))
    return ApiResult(
        invalid_token=invalid_token
    )


@bp.route("/get-expired-token")
def get_expired_token():
    return ApiResult(
        expired_token=create_access_token(identity='iamexpired@email.com', expires_delta=timedelta(seconds=1))
    )


@bp.route("/get-invalid-user-token")
def get_invalid_user_token():
    return ApiResult(
        invalid_token=create_access_token(identity='invaliduser@email.com', expires_delta=timedelta(days=30))
    )


@bp.route("/get-banned-user-token")
def get_banned_user_token():
    return ApiResult(
        banned_user_token=create_access_token(identity='banneduser@upr.edu', expires_delta=timedelta(days=30))
    )


@bp.route("/get-notapproved-user-token")
def get_notapproved_user_token():
    return ApiResult(
        notapproved_user_token=create_access_token(identity='notapproved@upr.edu', expires_delta=timedelta(days=30))
    )
