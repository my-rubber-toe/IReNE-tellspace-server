"""
create_app.py
====================================
Holds the configuration functions for blueprints, routes, cors, error catching and much more.
"""

from werkzeug.utils import find_modules, import_string
from flask import Flask, request, current_app, render_template

from utils.exceptions import TellSpaceError, TellSpaceAuthError, TellSpaceApiError
from utils.responses import ApiException, ApiResult
from marshmallow import ValidationError

from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import *

from flask_cors import CORS

from TS_DAOs import init_db


class ApiFlask(Flask):
    """
        Custom class extended from the Flask app object. 
        Overrides the make response method to add custom error classes ApiResult and ApiException support.
    """

    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            return rv.to_response()
        if isinstance(rv, ApiException):
            return rv.to_response()
        return Flask.make_response(self, rv)


def create_app(config=None):
    """Creates and returns a Flask app instance.

        Parameters
        ----------
            config
                the file to be used as the configuration file

        Returns
        -------
            app
                Instance of the ApiFlask class.
    """
    app = ApiFlask(__name__)

    with app.app_context():
        # Set all variables from the config file passed as a parameter
        app.config.from_object(config or {})

        # Setup Flask Secret Key
        app.secret_key = app.config['FLASK_SECRET_KEY']

        # Setup JWTManager to the app context on the attribute "jwt"
        app.config['JWT_BLACKLIST_ENABLED'] = True
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        app.__setattr__("jwt", JWTManager(app))

        # Setup CORS for cross site requests and more
        register_cors(app)

        # Setup and register blueprints to establish all endpoint routes
        register_blueprints(app)

        # Setup the error handlers
        register_error_handlers(app)

        # Setup and register '/ endpoint'
        register_base_url(app)

        # Setup app request teardown process if needed
        # register_request_teardown(app)

    return app


def register_blueprints(app: ApiFlask):
    """Register all blueprints under the {.blueprint} module in the passed application instance.

        Parameters
        ----------
            app
                the ApiFlask application instance.
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


def register_error_handlers(app: ApiFlask):
    """Register exception classes to flask application instance.

        Parameters
        ----------
            app
                the ApiFlask application instance.
    """
    if False:
        @app.errorhandler(TellSpaceError)
        def handle_error(error):
            return ApiException(
                error_type=error.__class__.__name__,
                message=error.error_stack,
                status=error.status
            )
    else:
        @app.errorhandler(TellSpaceApiError)
        def handle_api_error(error):
            return ApiException(
                error_type=error.__class__.__name__,
                message=error.msg,
                status=error.status
            )

        @app.errorhandler(TellSpaceAuthError)
        def handle_custom_errors(error):
            return ApiException(
                error_type=error.__class__.__name__,
                message=error.msg,
                status=error.status
            )

        # JWT Error Handler
        @app.errorhandler(JWTExtendedException)
        def request_token_errors(error):
            return ApiException(
                error_type='JWTTokenError',
                message=error.messages,
                status=error.status
            )

        @app.errorhandler(ValidationError)
        def request_validator_error(error):
            return ApiException(
                error_type='ValidationError',
                message=error.messages,
                status=400
            )

        @app.errorhandler(ValueError)
        def request_value_error(error):
            return ApiException(
                error_type='ValidationError',
                message=error.messages,
                status=400
            )

        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            TellSpaceError(
                err=error,
                msg='An unexpected error has occurred.',
                status=500
            )
            return ApiException(
                error_type='UnexpectedError',
                message=str(error),
                status=500
            )

        app.register_error_handler(
            400,
            lambda err: ApiException(message=str(
                err), status=400, error_type='Bad request')
        )

        app.register_error_handler(
            404,
            lambda err: ApiException(message=str(
                err), status=404, error_type='Not found')
        )

        app.register_error_handler(
            405,
            lambda err: ApiException(message=str(
                err), status=405, error_type='Request method')
        )


def register_base_url(app: ApiFlask):
    """
        Base url to perform server health check.

        Parameters
        ----------
            app
                the ApiFlask Instance
    """

    @app.route('/')
    def api():
        return ApiResult(message="Welcome to the TellSpace-Server API. Pleaer refer to the documentation.")


def register_request_teardown(app: ApiFlask):
    @app.teardown_request
    def do_the_thing(exeption):
        pass

    pass


def register_cors(app: ApiFlask):
    """
        Setup CORS, cross-origin-resource-sharing settings

        Parameters
        ----------
            app
                the ApiFlask application instance.
    """

    origins_list = '*'

    methods_list = ['GET', 'POST', 'PUT', 'DELETE','PATCH', 'OPTIONS']

    allowed_headers_list = [
        'Access-Control-Allow-Credentials',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Origin',
        'Content-Type',
        'Authorization',
        'Content-Disposition',
        'Referrer-Policy',
        'Strict-Transport-Security',
        'X-Frame-Options',
        'X-Xss-Protection',
        'X-Content-Type-Options',
        'X-Permitted-Cross-Domain-Policies'
    ]

    CORS(
        app=app,
        resources={r"/*": {"origins": origins_list}},
        methods=methods_list,
        allowed_headers=allowed_headers_list,
        supports_credentials=True
    )
