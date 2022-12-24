import traceback
from requests import Response, post
from flask import abort, render_template, make_response, redirect, request, url_for
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from app.users.repository import UserRepository
from app.users.models import UserModel
from blocklist import BLOCKLIST
from app.libs.mailgun import Mailgun
from app.libs.mailgun import MailGunException


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.mailgun = Mailgun()

    def send_confirmation_email(self, user_id:int, email:str) -> Response:
        #request.url_root[0:-1] = http://localhost:5000
        link = request.url_root[0:-1] + url_for("User", user_id=user_id)
        subject = "Registration confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
        return self.mailgun.send_email(email=[email], subject=subject, text=text, html=html)
    
    def register(self, user_data):
        if self.user_repository.get_user_by_email_or_username(user_data):
            abort(409, message="A user with that email or username already exists")
        
        user = UserModel(email=user_data["email"], password = pbkdf2_sha256.hash(user_data["password"]))
        try:
            self.user_repository.save(user)
            self.user_repository.commit()

            user = self.user_repository.get_user_by_email(email = user.email)
            self.send_confirmation_email( user_id = user.email, email = user.email)

        except MailGunException as e:

            self.user_repository.delete(user)
            self.user_repository.commit()
            return {"message": str(e)}, 500

        except:
            traceback.print_exc()
            return {"message":"Failed to create Account"}, 400

        return{"message": "Account created successfully, an email with the activation link has been sent to your emeil addresse, please check."}, 201
    
    def login(self, credentials):
        user = self.user_repository.get_user_by_email_or_username(credentials)

        if user and pbkdf2_sha256.verify(credentials["password"], user.password):
            if user.is_activated:

            # user.is_authenticated = True
                additional_claims = {"roles": user.roles}
                access_token = create_access_token(identity=user.id, additional_claims=additional_claims, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
            
                return {"access_token":access_token, "refresh_token":refresh_token}
            return {"message": f"You have not confirme registration, please check your email <{user.first_name}>."}, 400
        
        abort(401, message="invalid credentieals.")
    
    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def delete(self, user_id):   
        jwt =  get_jwt()
        if jwt.get("roles") and jwt.get("roles") == "user":
            abort(401, message= "User privilege required.") 
        try:
            user = self.user_repository.get_user_by_id(user_id)
            self.user_repository.delete(user)
            self.user_repository.commit()
            return{"message": "user deleted"}, 200
        except:
            abort(404, message=f"A user with id:{user_id} doesn't exist")
    
    def refresh_token(self):
        # curent_user = get_jwt().get("sub") même chose que le ligne qui suit, permet de retourner le cuurent user 
        # elle etourne un NONE s'il n'y a pas de current user
        curent_user = get_jwt_identity()
        new_token = create_access_token(identity=curent_user, fresh=False)
        # on ne peut que rafrechir le token une seule foi, voir ci dessous
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}

    def logout(self):
        # curent_user = get_jwt_identity()
        
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
    
    def create_user(self, user:UserModel):
        try:
            self.user_repository.save(user)
            self.user_repository.commit()
            return{"message": "user created successfully."}, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while creating user")
    
    def get_all_user(self):
        """
        Return all users
        :return: a list of user objects
        """
        return self.user_repository.get_all()

    def confirm_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404

        user.is_activated = True
        self.user_repository.save(user)
        self.user_repository.commit()
        # return redirect("http//localhost:5000", 302)  pour rediriger
        headers = {"Content-type": "text/html"}
        return make_response(render_template("confirmation_page.html", email = user.email), 200, headers)