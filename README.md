# IReNE-tellspace-server


## Dependencies
    1. Python 3.8.0    
    2. pip3 19.0.3
    3. python venv
    
## Setup Environment File

Create a **.env** file in the main directory of the project. This file contains the environmental information used by 
the server. The file must contain the following:

```.env
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1

# System port to use
PORT=<your-port>

# Database
DB_NAME=<database-name>
DB_HOST=<your-database-connection-string>

# Authorization
GOOGLE_OAUTH_CLIENT_ID=<your-google-client-id>
GOOGLE_OAUTH_CLIENT_SECRET=<your-google-client-secret>
OAUTHLIB_RELAX_TOKEN_SCOPE=true

# Set to true for testing purpouses
FLASK_SECRET_KEY=<some-string>
FLASK_SALT=<some-string>
```

This application uses Google oAuth as the authentication strategy for login.The variables for `GOOGLE_OAUTH_CLIENT_ID` 
and `GOOGLE_OAUTH_CLIENT_SECRET` require the creation on a google project on
the [Google Cloud Console](https://console.cloud.google.com/). Users must provide a valid Google idToken 
issued by the same `GOOGLE_OAUTH_CLIENT_ID` as in the server. The server will verify if the given idToken indeed was
issued by said `GOOGLE_OAUTH_CLIENT_ID`.

For instructions on how to create the credentials please follow this tutorial to generate client ID and client secret.

[Google oAuth Strategy](https://developers.google.com/adwords/api/docs/guides/authentication#webapp)

Please verify the route `/auth/login/<google-token>` within the file `authentication.py` within the blueprints package 
of this application for information on how the process is 

Once the credentials have been created, replace them in the environment file. 


## Development Setup: Linux Environment

Ensure that you have `Python 3.8.0` installed and have the `venv` package installed.Once you have cloned the repository 
locally, create a virtual environment by running ```python3 -m venv venv```. This will create a folder named **venv**. 

To access the virtual environment run ```source ./venv/bin/activate```. You will see that you terminal has a prefix 
```(venv)``` in the console line.

Install all dependencies with ```pip install -r requirements.txt```.

Once all has been set, run the server using `python app.py`.

## Development Setup: Windows Environment

Ensure that you have `Python 3.8.0` and `Pycharm` installed. Once you have cloned the repository locally, open the project in pycharm 
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

To access this project's documentation, access the directory `/docs/build/html/` and open the `index.html` file in the 
browser of your liking.

This project uses `sphinx` as the document generator package. To generate the documentation for this project, 
change directory to `/docs` and run `make html`. Once all the application has been built, access the directory 
`/docs/build/html/` and open the file `index.html` in your desired browser. 

**Note: To update the documentation generation files, please refer to https://www.sphinx-doc.org/en/master/usage/quickstart.html**


 
