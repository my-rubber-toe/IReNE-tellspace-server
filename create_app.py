"""
create_app.py
====================================
Holds the configuration functions for blueprints, routes, cors, error catching and much more.
"""

from werkzeug.utils import find_modules, import_string
from flask import Flask

from utils.exceptions import TellSpaceAuthError, TellSpaceApiError
from utils.responses import ApiException, ApiResult

from flask_jwt_extended import JWTManager
import sys, inspect

from flask_cors import CORS


class ApiFlask(Flask):
    """
        Custom class extended from the Flask app object. 
        Overrides the make response method to add custom error classes ApiResult and ApiException support.
    """

    def __init__(self, import_name):
        super().__init__(import_name)

    def make_response(self, rv):
        """
            Return a response object which you can use to attach headers and registers the ApiResult and ApiException
            classes as response objects.

            Returns
            -------
                    Instance of a Flask Response class.
        """
        if isinstance(rv, ApiResult):
            return rv.to_response()
        if isinstance(rv, ApiException):
            return rv.to_response()
        return Flask.make_response(self, rv)

    def create_app(self, config=None):
        """
            Sets up this class instance with the respective configuration.

            Parameters
            ----------
                config
                    the file to be used as the configuration file

            Returns
            -------
                self
                    Instance of the ApiFlask class.
        """

        with self.app_context():
            # Set all variables from the config file passed as a parameter
            self.config.from_object(config or {})

            # Setup Flask Secret Key
            self.secret_key = self.config['FLASK_SECRET_KEY']

            # Setup JWTManager to the app context on the attribute "jwt"
            self.config['JWT_BLACKLIST_ENABLED'] = True
            self.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
            self.__setattr__("jwt", JWTManager(self))

            # Setup CORS for cross site requests and more
            self.register_cors()

            # Setup and register blueprints to establish all endpoint routes
            self.register_blueprints()

            # Setup the error handlers
            self.register_error_handlers()

            # Setup and register '/ endpoint'
            self.register_base_url()

            return self

    def register_base_url(self):
        """
            Base url to perform server health check.

            Parameters
            ----------
                app
                    the ApiFlask Instance
        """

        @self.route('/')
        def api():
            return ApiResult(message="Welcome to the TellSpace-Server API. Please refer to the documentation.")

    def register_blueprints(self):
        """Register all blueprints under the {.blueprint} module in the passed application instance.

            Parameters
            ----------
                app
                    the ApiFlask application instance.
        """
        for name in find_modules('blueprints'):
            mod = import_string(name)
            if hasattr(mod, 'bp'):
                self.register_blueprint(mod.bp)

    def register_error_handlers(self):
        """Register all possible exception classes to this class instance. Exceptions taken into consideration are
            1. flask_jwt_extended.exceptions - All the JWT token related exceptions.
            2. marshmallow.exceptions

        """

        if(self.config['FLASK_DEBUG'] == 0):
            # Register JWT exceptions
            for name, obj in inspect.getmembers(sys.modules['flask_jwt_extended.exceptions']):
                if inspect.isclass(obj):
                    @self.errorhandler(obj)
                    def handle_jwt_excepions(error):
                        return ApiException(
                            error_type='TokenError',
                            message=error.msg,
                            status=error.status
                        )

            # Register marshmallow validator  exceptions
            for name, obj in inspect.getmembers(sys.modules['marshmallow.exceptions']):
                if inspect.isclass(obj):
                    @self.errorhandler(obj)
                    def handle_marshmallow_errors(error):
                        return ApiException(
                            error_type='ValidationError',
                            message='Please verify you request body and parameters.',
                            status=400
                        )

            # Register marshmallow validator  exceptions
            for name, obj in inspect.getmembers(sys.modules['mongoengine.errors']):
                if inspect.isclass(obj) and not name == 'defaultdict':
                    @self.errorhandler(obj)
                    def handle_database_errors(error):
                        return ApiException(
                            error_type='DatabaseError',
                            message='Internal Server Error',
                            status=500
                        )

            @self.errorhandler(TellSpaceApiError)
            def handle_api_error(error):
                return ApiException(
                    error_type='TellSpaceApiError',
                    message=error.msg,
                    status=error.status
                )

            @self.errorhandler(TellSpaceAuthError)
            def handle_custom_errors(error):
                return ApiException(
                    error_type='TellSpaceAuthError',
                    message=error.msg,
                    status=error.status
                )

            @self.errorhandler(ValueError)
            def request_value_error(error):
                return ApiException(
                    error_type='ValueError',
                    message=error.messages,
                    status=400
                )

            @self.errorhandler(Exception)
            def handle_unexpected_error(error):
                return ApiException(error_type='UnexpectedError', message=str(error), status=500)

            self.register_error_handler(
                400,
                lambda err: ApiException(message=str(
                    err), status=400, error_type='Bad request')
            )

            self.register_error_handler(
                404,
                lambda err: ApiException(message=str(
                    err), status=404, error_type='Not found')
            )

            self.register_error_handler(
                405,
                lambda err: ApiException(message=str(
                    err), status=405, error_type='Request method')
            )

    def register_cors(self):
        """
            Setup CORS, cross-origin-resource-sharing settings

            Parameters
            ----------
                app
                    the ApiFlask application instance.
        """

        origins_list = '*'

        methods_list = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

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
            app=self,
            resources={r"/*": {"origins": origins_list}},
            methods=methods_list,
            allowed_headers=allowed_headers_list,
            supports_credentials=True
        )
