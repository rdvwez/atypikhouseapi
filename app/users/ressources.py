from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from app.users.service import UserService
from app.users.models import UserModel
from schemas import UserSchema, UserRegisterSchema



blp = Blueprint("Users","users",description="Operations on users",url_prefix="/api")

@blp.route("/register")
class UserRegister(MethodView):

    # @inject
    def __init__(self):
        self.user_service = UserService()

    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        self.user_service.register(user_data)

@blp.route("/login")
class UserLogin(MethodView):

    # @inject
    def __init__(self):
        self.user_service = UserService()
    
    @blp.arguments(UserRegisterSchema)
    def post(self, credentials):
        return self.user_service.login(credentials)

@blp.route("/logout")
class UserLogout(MethodView):
    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    def post(self):
        return self.user_service.logout()


@blp.route("/refresh")
class TokeRefresh(MethodView):
    def __init__(self):
        self.user_service = UserService()

    @jwt_required(refresh=True)
    def post(self):
        self.user_service.refresh_token()

@blp.route("/user/<int:user_id>")
class User(MethodView):

    def __init__(self):
        self.user_service = UserService()

    @jwt_required() #peret de securiser la route, il faut avoir le token pour y acceder
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user
    
    @jwt_required()
    def delete(self, user_id):
        return self.user_service.delete(user_id)


@blp.route("/user")
class UserList(MethodView):

    
    def __init__(self):
        self.user_service = UserService()

    #TODO: Ne peut qu'aaccer à cette routr l'admin connecté
    @jwt_required() 
    @blp.response(200, UserSchema(many=True))
    def get(self):
        # return "ERT"
        return self.user_service.get_all_user()

    #TODO: Ne peut acceder à cette route l'admin connecté
    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, user_data):
        user= UserModel(**user_data)
        self.user_service.create_user(user)
        return user

@blp.route("/user_confirm/<int:user_id>")
class UserConfirm(MethodView):

    def __init__(self):
        self.user_service = UserService()

    @jwt_required() 
    # @blp.response(200, UserSchema)
    def get(self, user_id):
        return self.user_service.confirm_user(user_id)

@blp.route("/user/password")
class SetPassword(MethodView):

    def __init__(self):
        self.user_service = UserService()
    
    @jwt_required(fresh=True)
    @blp.arguments(UserSchema)
    def post(self):
        user_json = request.get_json()
        # user_data = user_schema.load()
        self.user_service.set_password(user_json)
