"""
app.py
====================================
Main file that holds the entry point for this server application. To run this server in development
creating flask app instance. Parameters could be used depending on the files present
in `pwd`/config/ directory of this project. Example "config.environment", "config.development"

Depending on that input the app will be initialized with the corresponding environmental variables.
"""

from create_app import ApiFlask


if __name__ == '__main__':

    app = ApiFlask(__name__).create_app('config.environment')
    app.run(host='localhost', port=app.config['PORT'], debug=app.config['FLASK_DEBUG'])