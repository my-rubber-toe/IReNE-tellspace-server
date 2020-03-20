# IReNE-tellspace-server


## Dependencies
    1. Python 3.8.0
    2. flask
    3. flask-cors
    3. flask-dance
    4. flask-jwt-extended
    5. marshmallow
    6. werkzeug
    7. python-dotenv
    8. commitizen
    

## Development Setup: Terminal

Clone the repository locally and create a virtual environment using ```python -m venv venv```. 
This will create a folder named **venv**. To access the virtual environment run ```source ./venv/bin/activate```.
You will see that you terminal has a prefix ```(venv)``` in the console line.

Install all dependencies with ```pip install -r requirements.txt```.

Create a **.env** file in the main directory of the project. The file must contain the following:

```.env
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1

# System port to use
PORT=5000

# Database TBD
DB = ''

# Authorization
GOOGLE_OAUTH_CLIENT_ID="your-google-client-id"
GOOGLE_OAUTH_CLIENT_SECRET="your-google-client-secret"
OAUTHLIB_RELAX_TOKEN_SCOPE=true
OAUTHLIB_INSECURE_TRANSPORT=true
FLASK_SECRET_KEY="your-server-secret-key" 
FLASK_SALT="your-server-salt"
```

## Development Setup: Pycharm

Open the project in pycharm and set your interpreter to use the installed version of
Python. For more info follow this link https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html


 
