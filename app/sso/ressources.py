from flask import g, request, url_for
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import google

from app.users.repository import UserRepository
from app.users.models import UserModel


blp = Blueprint("Sso",__name__,description="Operations on sso login")


@blp.route("/login/google" )
class GoogleLogin(MethodView):

    def get(self):
        return google.authorize(callback=url_for(".google_authorized", _external=True))
        # return google.authorize(callback="localhost:500/login/google/authorized")


@blp.route("/login/google/authorized", endpoint="google_authorized")
class GoogleAuthorized(MethodView):
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get(self):
        resp = google.authorized_response()
        return 'toti'

        if resp is None:
            error_reponse = {
                "error": request.args["error"],
                "error_description": request.args["error_descripton"]
            }
        user_info = google.get("userinfo")

        user = self.user_repository.get_user_by_email_or_username( {"email":user_info.data.get("email")})
        if not user:
            user =  UserModel(
                email = user_info.data.get("email"),
                password = None,
            )
        access_token = create_access_token(identity=user.id, fresh= True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token":refresh_token}, 200


