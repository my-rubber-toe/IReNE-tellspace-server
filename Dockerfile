FROM python:3.8.0

ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

ENV PORT=5000

# Database
ENV DB = ''

# Authorization
ENV GOOGLE_OAUTH_CLIENT_ID=125759116505-flugvdnnv7lm6q6htj62uic5ut70e594.apps.googleusercontent.com
ENV GOOGLE_OAUTH_CLIENT_SECRET=eHJTs2-KrUEBiyXC9E5r1y3D
ENV OAUTHLIB_RELAX_TOKEN_SCOPE=true
ENV OAUTHLIB_INSECURE_TRANSPORT=true
ENV FLASK_SECRET_KEY ='SuperSecretKeyThatNobodyCanCrack'
ENV FLASK_SALT='IamAnotherSaltyHuman'

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "./app.py"]
