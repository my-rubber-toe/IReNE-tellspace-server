from werkzeug.utils import find_modules, import_string
from flask import Flask, request, current_app

from utils.exceptions import TellSpaceError, TellSpaceAuthError, TellSpaceApiError
from utils.responses import ApiException, ApiResult
from marshmallow import  ValidationError


from flask_cors import CORS


class ApiFlask(Flask):
    """
        Custom class extended from the Flask app object. 
        Overrides the make response method to add custom error classes ApiResult and ApiException support  
    """
    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            return rv.to_response()
        if isinstance(rv, ApiException):
            return rv.to_response()
        return Flask.make_response(self, rv)


def create_app(config=None):
    """Creates and returns a Flask app instance.

    Keyword Arguments:
        config {string} --  (default: {None})

    Returns:
        [flask_application] -- instance of a flask app
    """
    app = ApiFlask(__name__)

    with app.app_context():
        # Set all variables from the config file passed as a parameter
        app.config.from_object(config or {})

        # Setup Flask Secret Key
        app.secret_key = app.config['FLASK_SECRET_KEY']

        # TODO: Setup CORS for all endpoints
        # register_cors(app)

        # TODO: Setup database configuration
        # db.init_app(app)

        # TODO: Setup authentication strategy for Google oAuth
        # auth_setup.init_app(app)

        # Setup validator plugins
        # validator.init_app(app)

        # Setup blueprints to establish all endpoint routes
        register_blueprints(app)

        # Register the error handlers
        register_error_handlers(app)

        # register '/api endpoint'
        # register_base_url(app)

        # Setup app request teardown process
        register_request_teardown(app)

        return app


def register_blueprints(app: ApiFlask):
    """Register all blueprints under the {.blueprint} module in the passed application instance. The authentication
        blueprint will be treated differently

    Arguments:
        app {flask application} -- application instance
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


def register_error_handlers(app: ApiFlask):
    """Register error daos to flask application instance.

    Arguments:
        app {flask application} -- application instance
    """
    if app.config['FLASK_DEBUG']:
        @app.errorhandler(TellSpaceError)
        def handle_error(error):
            return ApiException(
                error_type=error.__class__.__name__,
                message=error.error_stack,
                status=error.status
            )

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

    @app.errorhandler(TellSpaceError)
    def handle_general_error(error):
        return ApiException(
            error_type=error.__class__.__name__,
            message=error.error_stack,
            status=500
        )

    @app.errorhandler(ValidationError)
    def request_validator_error(err):
        return ApiException(
            error_type='ValidationError',
            message=err.messages,
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
            error_type='UnexpectedException',
            message='An unexpected error has occurred. Please verify error logs',
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


def register_base_url(app: Flask):
    @app.route('/api/')
    def api():
        return ApiResult(
            {
                'message': 'You have reached the TellSpace API. To make other requests please use all routes under /api'
            },
            status=200
        )


def register_request_teardown(app: ApiFlask):
    @app.teardown_request
    def do_the_thing(exeption):
        pass
    pass


def register_cors(app: ApiFlask):
    """
        Setup CORS , cross-origin-resource-sharing settings
    """

    origins_list = '*'

    methods_list = ['GET', 'POST', 'PUT', 'PATCH', 'OPTIONS']

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
        resources={r"/api/*": {"origins": origins_list}},
        methods=methods_list,
        allowed_headers=allowed_headers_list,
        supports_credentials=True
    )
