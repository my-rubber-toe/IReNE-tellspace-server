"""Use this class as you testing playground"""


from flask import Blueprint, g, current_app, request, session, make_response, jsonify
from utils.responses import ApiResult, ApiException
from datetime import timedelta

from flask_jwt_extended import jwt_required, create_access_token, \
    create_refresh_token, get_jwt_identity, jwt_refresh_token_required, get_raw_jwt


route_prefix = '/api/test'

bp = Blueprint('test', __name__, url_prefix=route_prefix)

blacklist = set()


@current_app.jwt.token_in_blacklist_loader
def check_if_token_in_blacklist_test(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


# Standard login endpoint
@bp.route('/login', methods=['GET'])
def login():
    ret = {
        'access_token': create_access_token(identity=321, expires_delta=timedelta(seconds=30)),
        'refresh_token': create_refresh_token(identity=321, expires_delta=timedelta(seconds=30))
    }
    return jsonify(ret), 200


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
@bp.route('/refresh')
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@bp.route('/logout')
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    print(blacklist)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@bp.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    print(blacklist)
    return jsonify({"msg": "Successfully logged out"}), 200


# This will now prevent users with blacklisted tokens from
# accessing this endpoint
@bp.route('/me', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


@bp.before_request
def before_requests():
    print('Before requests in /api/test/')

