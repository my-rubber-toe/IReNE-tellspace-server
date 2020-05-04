"""
app.py
Main file that holds the entry point for this server application.
"""

from create_app import create_app
'''
To run this server in development
    $ export FLASK_APP=`pwd`/app.py
    $ export FLASK_DEBUG=1
creating flask app instance

parameters could be
    config.development
    config.testing
    config.production

depending on that input the app will be initialized with the
corresponding database queries files and database driver
'''

# Set config file accordingly
app = create_app('config.development')

if __name__ == '__main__':
    app.run(host='localhost', port=app.config['PORT'], debug=app.config['FLASK_DEBUG'])
