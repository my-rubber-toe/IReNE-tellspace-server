# TODO: Implement authentication strategy with flask dance and Google oAuth. Use decorators as needed.


from flask import Blueprint, g, current_app, request, session, make_response, jsonify
from utils.responses import ApiResult, ApiException

from uuid import uuid4

route_prefix = f'{current_app.config["PREFIX_URL"]}/auth'

bp = Blueprint('auth', __name__, url_prefix=route_prefix)


@bp.route('/login')
def auth_login():
    """ Objective:
           Perform the authorization strategy sequence. Contact Google oAuth to perform sign in sequence accordingly.

        Pre-conditions:
           Client has no session token.
           Client has invalid session token.

        Args:
           None

        Returns:
          ApiResult object with a new session token.

        Author:
           Roberto Y. Guzman

        Date:
          March 16, 2020
    """

    return ApiResult(
        value={
            "response": f'Hi, your new session token is {uuid4()}'
        }
    )
