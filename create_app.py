"""
create_app.py
====================================
Holds the configuration functions for blueprints, routes, cors, error catching and much more.
"""

from werkzeug.utils import find_modules, import_string
from flask import Flask
from flask_cors import CORS
from utils.exceptions import TellSpaceAuthError, TellSpaceApiError
from utils.responses import ApiException, ApiResult
from utils.scheduled_jobs import ScheduledJobs
from flask_jwt_extended import JWTManager
import sys, inspect
from database.db_init import register_database


class ApiFlask(Flask):
    """
        Custom class extended from the Flask app object. 
        Overrides the make response method to add custom error classes ApiResult and ApiException support.

        Parameters
        ----------
            import_name
                name to give the parent class of Flask
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
            Sets up this class instance by configuring database connections, endpoints, cors, secrets, origins, error
            handlers and JWT manager.

            Parameters
            ----------
                config
                    the file to be used as the configuration file

            Returns
            -------
                ApiFlask
                    Instance of the ApiFlask class to be used as the entry object of this application.
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
            self.__register_cors()

            # Setup and register blueprints to establish all endpoint routes
            self.__register_blueprints()

            # Setup the error handlers
            self.__register_error_handlers()

            # Setup and register '/ endpoint'
            self.__register_base_url()

            # Register database
            register_database(self)

            # Register ScheduledJobs
            ScheduledJobs.job_ping_db()

            return self

    def __register_base_url(self):
        """Base url to perform server health check."""

        @self.route('/')
        def api():
            return ApiResult(message="TellSpace Server: OK")

    def __register_blueprints(self):
        """Register all blueprints under the {.blueprint} module in the passed application instance."""
        for name in find_modules('blueprints'):
            mod = import_string(name)
            if hasattr(mod, 'bp'):
                self.register_blueprint(mod.bp)

    def __register_cors(self):
        """Setup CORS, cross-origin-resource-sharing settings."""

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

    def __register_error_handlers(self):
        """Register all possible exception classes to this class instance. Exceptions taken into consideration are
            1. flask_jwt_extended.exceptions - exception classes for JWT token related exceptions.
            2. marshmallow.exceptions - exceptions classes for parameter and request body validation errors.
            3. mongoengine.errors - exception classes for database related requests.
        """

        # Register JWT exceptions
        for name, obj in inspect.getmembers(sys.modules['flask_jwt_extended.exceptions']):
            if inspect.isclass(obj):
                @self.errorhandler(obj)
                def handle_jwt_excepions(error):
                    return ApiException(
                        error_type='Token Error',
                        message=error.msg,
                        status=error.status
                    )

        # Register marshmallow validator  exceptions
        for name, obj in inspect.getmembers(sys.modules['marshmallow.exceptions']):
            if inspect.isclass(obj):
                @self.errorhandler(obj)
                def handle_marshmallow_errors(error):
                    return ApiException(
                        error_type='Validation Error',
                        message='Please verify you request body and parameters.',
                        status=400
                    )

        # Register mongoengine  exceptions
        for name, obj in inspect.getmembers(sys.modules['mongoengine.errors']):
            if inspect.isclass(obj) and not name == 'defaultdict':
                @self.errorhandler(obj)
                def handle_database_errors(error):
                    return ApiException(
                        error_type='Database Error',
                        message='Internal Server Error',
                        status=500
                    )

        @self.errorhandler(TellSpaceApiError)
        def handle_api_error(error):
            return ApiException(
                error_type=error.error_type,
                message=error.msg,
                status=error.status
            )

        @self.errorhandler(TellSpaceAuthError)
        def handle_custom_errors(error):
            return ApiException(
                error_type=error.error_type,
                message=error.msg,
                status=error.status
            )

        @self.errorhandler(ValueError)
        def request_value_error(error):
            return ApiException(
                error_type='Value Error',
                message=error.messages,
                status=400
            )

        @self.errorhandler(Exception)
        def handle_unexpected_error(error):
            return ApiException(error_type='Unexpected Error', message=str(error), status=500)

        self.register_error_handler(
            400,
            lambda err: ApiException(message=str(
                err), status=400, error_type='Bad Request')
        )

        self.register_error_handler(
            404,
            lambda err: ApiException(message=str(
                err), status=404, error_type='Not Found')
        )

        self.register_error_handler(
            405,
            lambda err: ApiException(message=str(
                err), status=405, error_type='Request Method')
        )

        self.register_error_handler(
            422,
            lambda err: ApiException(message=str(
                err), status=422, error_type='Unprocessable Entity')
        )
