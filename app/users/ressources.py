from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from app.users.service import UserService
from app.libs.decorators import owner_required, admin_required, customer_required
from app.users.models import UserModel
from schemas import UserSchema, UserRegisterSchema, UserPasswordSetSchema, UserLoginSchema, UserRefreshTokenSchema



blp = Blueprint("Users","users",description="Operations on users",url_prefix="/api")

@blp.route("/register")
class UserRegister(MethodView):

    # @inject
    def __init__(self):
        self.user_service = UserService()

    @blp.arguments(UserRegisterSchema)
    @blp.doc(tags=['Users'], security=[{}])
    def post(self, user_data):
        """User register route

        Args:
            user_data (dict): user data when registering, login and password

        Returns:
            str: message confirmin the registration or error
        """
        return self.user_service.register(user_data)

@blp.route("/login")
class UserLogin(MethodView):

    # @inject
    def __init__(self):
        self.user_service = UserService()
    
    @blp.arguments(UserRegisterSchema)
    @blp.response(200, UserLoginSchema)
    @blp.doc(tags=['Users'], security=[{}])
    def post(self, credentials):
        """Log in Route

        Args:
            credentials (dict): user credentials when logging in, (email and password)

        Returns:
            str: user token or error massage
        """
        return self.user_service.login(credentials)

@blp.route("/logout")
class UserLogout(MethodView):
    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    # @blp.response(200, UserLogoutSchema)
    # @blp.doc(tags=['Users'], security=[{}])
    def get(self):
        """logout route

        Returns:
            str: Message confirming the logout
        """
        return self.user_service.logout()


@blp.route("/refresh")
class TokeRefresh(MethodView):
    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    @blp.response(200, UserRefreshTokenSchema)
    # @blp.doc(tags=['Users'], security=[{}])
    def get(self):
        """Refresh Token

        Returns:
            str: new token
        """
        return self.user_service.refresh_token()

@blp.route("/user/<int:user_id>")
class User(MethodView):

    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    # @blp.doc(tags=['Users'], security=[{}])
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """get user

        Args:
            user_id (int): User id

        Returns:
            User: User data
        """
        return self.user_service.get_user_by_id(user_id)

    
    @jwt_required()
    def delete(self, user_id):
        """delete user

        Args:
            user_id (int): User id

        Returns:
            str: delation confirmation message or error
        """
        return self.user_service.delete(user_id)


@blp.route("/user")
class UserList(MethodView):

    
    def __init__(self):
        self.user_service = UserService()
        
    @jwt_required() 
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get list of user

        Returns:
            dict: Liste of user
        """
        # return "ERT"
        return self.user_service.get_all_user()

    #TODO: Ne peut acceder à cette route l'admin connecté
    @jwt_required(fresh=True)
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, user_data):
        """Create user

        Args:
            user_data (dict): user data dictionary

        Returns:
            str: creation confirmation
        """
        user= UserModel(**user_data)
        self.user_service.create_user(user)
        return user

@blp.route("/user_confirm/<int:user_id>")
class UserConfirm(MethodView):

    def __init__(self):
        self.user_service = UserService()

    # @jwt_required() 
    # @blp.response(200, UserSchema)
    @blp.doc(tags=['Users'], security=[{}])
    def get(self, user_id):
        """Confirm user Account

        Args:
            user_id (int): Id for user, confirming his accout

        Returns: Send the confirm email
        """
        return self.user_service.confirm_user(user_id)

@blp.route("/user/me")
class CurrentUser(MethodView):

    def __init__(self):
        self.user_service = UserService()

    @jwt_required(fresh=True)
    @blp.response(200, UserSchema)
    # @blp.doc(tags=['Users'], security=[{}])
    def get(self):
        """Get current user


        Returns: A current user object
        """
        return self.user_service.get_current_uer()

@blp.route("/user/password")
class SetPassword(MethodView):

    def __init__(self):
        self.user_service = UserService()
    
    @jwt_required(fresh=True)
    @blp.arguments(UserPasswordSetSchema)
    @blp.response(201, UserSchema)
    def post(self,user_data):
        """Change user Password

        Args:
            user_data (dict): dictionary containing the new password

        Returns:
            _type_: The updated user
        """
        return self.user_service.set_password(user_data)

