# IReNE-tellspace-server


## Dependencies
    1. Python 3.8.0    
    2. pip3 19.03

## Development Setup: Linux Environment

Ensure that you have `Python 3.8.0` installed. Once you have cloned the repository locally, create a virtual environment
by running ```python3 -m venv venv```. This will create a folder named **venv**. 

To access the virtual environment run ```source ./venv/bin/activate```. You will see that you terminal has a prefix 
```(venv)``` in the console line.

Install all dependencies with ```pip install -r requirements.txt```.

Create a **.env** file in the main directory of the project. This file contains the evironmental information used by the
server. The file must contain the following:

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

# Set to true for testing purpouses
OAUTHLIB_INSECURE_TRANSPORT=true
FLASK_SECRET_KEY="your-server-secret-key" 
FLASK_SALT="your-server-salt"
```

Once all has been set, run the server using `flask run` or `python app.py`.

## Development Setup: Pycharm

Ensure that you have `Python 3.8.0` installed. Once you have cloned the repository locally, open the project in pycharm 
and access the project settings. 

1. Search for `Project Interpreter`. 
2. Click on the Project interpreter dropdown and select `Show All`. 
3. Click on the `+` sign to add a new project interpreter. 
4. Select `Virtual Environment` and make sure that the base interpreter is `Python 3.8.0`.
5. Click `OK` and the system should start installing all project dependencies.

**Note: if dependencies are not installed automatically, open a terminal and run `pip install -r requirements.txt`.**

When all dependencies have been installed, right-click on the `app.py` file and run. You can also open a terminal and 
run `python app.py`

For more info follow this link https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html


## Documentation

To generate the documentation for this project, change directory to `/docs` and run `make html`. Once all the 
application has been built, access the directory `/docs/build/html/` and open the file `index.html` in
your desired browser. 

**Note: To update the documentation files, please refer to https://www.sphinx-doc.org/en/master/usage/quickstart.html**


 
