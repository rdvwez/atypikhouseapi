import logging
from app.images.models import ImageModel
from flask import g, request, url_for, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
from app.libs.oa import google, facebook, github
from flask_oauthlib.client import OAuth, OAuthException
import default_config as dc

from app.users.repository import UserRepository
from app.users.models import UserModel
from app.users.service import UserService
from app.images.service import ImageService


blp = Blueprint("Sso",__name__,description="Operations on sso login",url_prefix="/api")

oauth = OAuth()

google = oauth.remote_app(
    'google',
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method="POST",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    consumer_key= dc.GOOGLE_OAUTH_CLIENT_ID,
    consumer_secret=dc.GOOGLE_OAUTH_CLIENT_SECRET,
    request_token_params={'scope': ['email', 'profile']}
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=dc.FACEBOOK_CONSUMMER_KEY,
    consumer_secret=dc.FACEBOOK_CONSUMMER_SECRET,
    request_token_params={'scope': ['email', 'user_friends']}

)

@google.tokengetter
def get_google_token():
    return g.access_token

@blp.route("/login/google")
class GoogleLogin(MethodView):

    def get(self):
        redirect_uri = url_for(".google_authorized",_external=True)
        return oauth.google.authorize(redirect_uri)

@blp.route("/login/facebook")
class FacebookLogin(MethodView):

    def get(self):
        redirect_uri = url_for(".facebook_authorized",_external=True)
        return oauth.facebook.authorize(redirect_uri)

@blp.route("/login/github")
class GithubLogin(MethodView):

    def get(self):
        return github.authorize(callback=url_for(".github_authorized", _external=True))


@blp.route("/login/google/authorized", endpoint="google_authorized")
class GoogleAuthorized(MethodView):

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_service = UserService()
        self.image_service = ImageService()

    def get(self):
        resp = google.authorized_response()


        if resp is None or resp.get('access_token') is None:
            return {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
        
        # Vérifier que l'utilisateur a autorisé l'application
        # if resp.get('error'):
        #     return {
        #         "error": resp.get('error'),
        #         "error_description": resp.get('error_description')
        #     }

        # Stockez l'access_token dans l'utilisateur (g.user dans ce cas)
        g.access_token = (resp['access_token'], '')

        # Utilisez l'access_token pour récupérer des informations supplémentaires
        user_info = google.get("userinfo")
        # try:
        #     user_info = google.get("userinfo")
        # except OAuthException as e:
        #     logging.error(e)
        #     print(f"OAuthException: {e}")

        # Maintenant, user_info contient des informations telles que l'email
        # email = user_info.data.get("email")

        # Reste du code pour traiter les informations récupérées

        # return {"email": email, "other_data": user_info.data}, 200
        
        # token = resp['access_token']
        # token = google.authorize_access_token()
        # resp = google.get('account/verify_credentials.json')
        # resp.raise_for_status()
        # resp = google.get('userinfo')
        # resp = oauth.google.get('account/verify_credentials.json')
        # resp.raise_for_status()
        # profile = resp.json()
        # logging.debug(resp)
        # logging.error(user_info.data)
        # print(user_info.data)
        

        user = self.user_repository.get_user_by_email_or_username({"email": user_info.data.get("email")})

        if not user:
            user = UserModel(
                email=user_info.data.get("email"),
                password=None,
                name = user_info.data.get("family_name"),
                firstname = user_info.data.get("given_name"),
                is_customer = True,
                is_activated=True
            )
            self.user_repository.save(user)
            self.user_repository.commit()

            image = ImageModel(path=user_info.data.get("picture"), user_id=user.id)
            saved_image = self.image_service.create_image(image)

        access_token, refresh_token = self.user_service.generate_token(user)

        user.refresh_token = refresh_token

        self.user_repository.save(user)
        self.user_repository.commit()

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
        # return  user_info.data, 200

@blp.route("/login/callback", endpoint="facebook_authorized")
class FacebookAuthorized(MethodView):
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get(self):
        # resp = facebook.authorized_response()

        # if resp is None:
        #     return {
        #         "error": request.args["error"],
        #         "error_description": request.args["error_descripton"]
        #     }
        # user_info = facebook.get("userinfo")

        token = oauth.facebook.authorize_access_token()
        resp = oauth.facebook.get('account/verify_credentials.json')
        resp.raise_for_status()
        profile = resp.json()
        user_info = facebook.get('/me')
        # do something with the token and profile
        return profile

        # user = self.user_repository.get_user_by_email_or_username( {"username":user_info.data.get("name")})
        # if not user:
        #     user =  UserModel(
        #         email = user_info.data.get("email"),
        #         password = None,
        #     )
        # access_token = create_access_token(identity=user.id, fresh= True)
        # refresh_token = create_refresh_token(user.id)

        # return {"access_token": access_token, "refresh_token":refresh_token}, 200



@blp.route("/login/github/authorized", endpoint="github_authorized")
class GithubAuthorized(MethodView):
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get(self):
        resp = github.authorized_response()

        if resp is None:
            return {
                "error": request.args["error"],
                "error_description": request.args["error_descripton"]
            }
        
        g.access_token = resp.get("access_token")
        user_info = github.get("user")
        githubusername = user_info.data.get("login")

        user = self.user_repository.get_user_by_email_or_username( {"username":githubusername})
        if not user:
            user =  UserModel(
                email = user_info.data.get("email"),
                password = None,
            )

        access_token = create_access_token(identity=user.id, fresh= True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token":refresh_token}, 200