import os
from flask import g
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app('github',
    base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    consumer_key=os.getenv("GITHUB_COSUMMER_KEY"),
    consumer_secret=os.getenv("GITHUB_COSUMMER_SECRET"),
    request_token_params={"scope":"user:email"},
    request_token_url=None,
    access_token_method="POST"
)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<your key here>',
    consumer_secret='<your secret here>'
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="783711930077559",
    consumer_secret="c61a6247a34c6db886705cbf2c9feb4b",
    request_token_params={'scope': 'email'}

)

google = oauth.remote_app(
    'google',
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method="POST",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    consumer_key= "794179832332-3jkq8ia1ng9s4ej8q36c83umd05p6r1g.apps.googleusercontent.com",
    consumer_secret="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",
    request_token_params={'scope': 'email'}
)


@twitter.tokengetter
def get_twitter_token():
    if "access_token" in g:
        return g.access_token

@google.tokengetter
def get_google_token():
    if "access_token" in g:
        return g.access_token

@facebook.tokengetter
def get_facebook_token():
    if "access_token" in g:
        return g.access_token

@github.tokengetter
def get_github_token():
    if "access_token" in g:
        return g.access_token