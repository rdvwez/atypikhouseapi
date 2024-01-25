import sys
from typing import Dict, Tuple
import traceback
import smtplib
import os
from datetime import timedelta

from requests import Response, post
from flask import abort, render_template, make_response, redirect, request, url_for
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.libs.decorators import owner_required, admin_required, customer_required

from app.users.repository import UserRepository
from app.users.models import UserModel
from blocklist import BLOCKLIST
from app.libs.mailgun import Mailgun
from app.libs.mailgun import MailGunException
from app.libs.email_sender import send_confirmation_account_mail


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.mailgun = Mailgun()

    # def send_confirmation_mail(self, user_id:int, email:str):
    #     # breakpoint()
    #     # print(os.environ.get('SMPT_SERVER'))
    #     link = request.url_root[0:-1] + url_for("Users.UserConfirm",user_id = user_id)
    #     subject = "Registration confirmation"
    #     text = f"Please click the link to confirm your registration: {link}"
    #     html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
        
    #     message = MIMEMultipart("alternative")
    #     message["From"] = os.environ.get('FROM_ADDR')
    #     message["To"] = email
    #     message["Subject"] = subject

    #     part1 = MIMEText(text, "plain")
    #     part2 = MIMEText(html, "html")

    #     message.attach(part1)
    #     message.attach(part2)
    #     # breakpoint()
    #     err=None
    #     try:
    #         # Connexion au serveur SMTP
    #         server = smtplib.SMTP(os.environ.get('SMPT_SERVER'), os.environ.get('SMTP_PORT'))
            
    #         server.starttls()
    #         server.login(os.environ.get('SMTP_LOGIN'), os.environ.get('SMTP_PASSWORD'))

    #         # Envoi du message
    #         server.sendmail(os.environ.get('FROM_ADDR'), email, message.as_string())
    #         # print("E-mail envoyé avec succès !")
    #         # breakpoint()

    #     except Exception as e:
    #         err = e
    #         print("Une erreur s'est produite lors de l'envoi de l'e-mail : ", e)
    #     except KeyboardInterrupt as er:
    #         # err = er
    #         err = traceback.print_exc(file=sys.stdout)
    #         # breakpoint()

    #     finally:
    #         # Fermeture de la connexion SMTP
    #         if 'server' in locals():
    #             server.quit()
    #     return err

        # return self.mailgun.send_email(email=[email], subject=subject, text=text, html=html)
        # my_variable_value = os.environ.get('SMPT_SERVER')
        # SMTP_PORT=
        # SMTP_LOGIN=
        # SMTP_PASSWORD=

    # def send_confirmation_mail(self, user_id:int, email:str) -> Response:
    #     #request.url_root[0:-1] = http://localhost:5000
    #     link = request.url_root[0:-1] + url_for("Users.UserConfirm",user_id = user_id)
    #     subject = "Registration confirmation"
    #     text = f"Please click the link to confirm your registration: {link}"
    #     html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
    #     return self.mailgun.send_email(email=[email], subject=subject, text=text, html=html)
    
    def get_current_uer(self)-> UserModel:
        curent_user_id = get_jwt_identity()
        return self.user_repository.get_user_by_id(curent_user_id)

    def register(self, user_data):
        if self.user_repository.get_user_by_email_or_username(user_data):
            abort(409, message="A user with that email or username already exists")
        
        user = UserModel(email=user_data["email"], password = pbkdf2_sha256.hash(user_data["password"]))
        # try:
        self.user_repository.save(user)

        user = self.user_repository.get_user_by_email(email = user.email)
        # res = self.send_confirmation_mail( user_id = user.id, email = user.email)
        return{"message": "Account created successfully, an email with the activation link has been sent to your emeil addresse, please check."}, 201
        # res = send_confirmation_account_mail( user_id = user.id, email = user.email, subject="Registration confirmation", url_suffix="Users.UserConfirm")
        # if res is None:
        #     return{"message": "Account created successfully, an email with the activation link has been sent to your emeil addresse, please check."}, 201
        # else:

        #     self.user_repository.delete(user)
        #     self.user_repository.commit()
        #     return {"message": str(res)}, 500
    
    def generate_token(self, user: UserModel)-> Tuple[str, str]:
        token_duration = timedelta(hours=1)
        additional_claims = {"id": user.id, "is_customer": user.is_customer, "is_owner": user.is_owner, "is_admin": user.is_admin}
        # additional_claims = {"is_customer": user.is_customer, "is_owner":user.is_owner, "is_admin":user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims, fresh=True, expires_delta=token_duration)
        refresh_token = create_refresh_token(identity=user.id)

        return access_token, refresh_token
    
    def generate_temp_token(self, user: UserModel)->  str:
        token_duration = timedelta(minutes=5)
        additional_claims = {"id": user.id}
        temp_token = create_access_token(identity=user.id, additional_claims=additional_claims, fresh=True, expires_delta=token_duration)

        return temp_token
    
    def login(self, credentials:Dict[str,str]):
        user = self.user_repository.get_user_by_email_or_username(credentials)
        # breakpoint()
        if user and pbkdf2_sha256.verify(credentials["password"], user.password):
            if user.is_activated:

            # user.is_authenticated = True
                # additional_claims = {"id": user.id, "is_customer": user.is_customer, "is_owner": user.is_owner, "is_admin": user.is_admin}
                # additional_claims = {"is_customer": user.is_customer, "is_owner":user.is_owner, "is_admin":user.is_admin}
                # access_token = create_access_token(identity=user.id, additional_claims=additional_claims, fresh=True)
                # refresh_token = create_refresh_token(identity=user.id)
                access_token, refresh_token = self.generate_token(user)
                user.refresh_token = refresh_token

                self.user_repository.save(user)
                self.user_repository.commit()
                # return {"access_token":access_token}
                return {"access_token":access_token, "refresh_token":refresh_token}
            return {"message": f"You have not confirme registration, please check your email <{user.firstname}>."}, 400
        
        abort(401, "invalid credentieals.")
        
    @admin_required
    def get_user_by_id(self, user_id)-> UserModel:
        return self.user_repository.get_user_by_id(user_id)

    @admin_required
    def delete(self, user_id):   
        # jwt =  get_jwt()
        # if jwt.get("roles") and jwt.get("roles") == "user":
        #     abort(401, message= "User privilege required.") 
        try:
            user = self.user_repository.get_user_by_id(user_id)
            self.user_repository.delete(user)
            self.user_repository.commit()
            return{"message": "user deleted"}, 200
        except:
            abort(404, description=f"A user with id:{user_id} doesn't exist")

    @customer_required
    def refresh_token(self):
        # curent_user = get_jwt().get("sub") même chose que le ligne qui suit, permet de retourner le cuurent user 
        # elle etourne un NONE s'il n'y a pas de current user
        curent_user_id = get_jwt_identity()
        user = self.user_repository.get_user_by_id(curent_user_id)
        if not user:
            abort(401, "user not found")
        
        new_token, refresh_token = self.generate_token(user)
        user.refresh_token = refresh_token

        self.user_repository.save(user)
        self.user_repository.commit()
        # on ne peut que rafrechir le token une seule foi, voir ci dessous
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token,"refresh_token": refresh_token }, 200
        
        
    
    @customer_required
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

    @admin_required
    def get_all_user(self):
        """
        Return all users
        :return: a list of user objects
        """
        return self.user_repository.get_all()

    def confirm_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user :
            return {"message": "user not found"}, 404
        
        if user.is_activated:
            return {"message": "Account already confirmed"}, 400

        user.is_activated = True
        self.user_repository.save(user)
        self.user_repository.commit()
        # return redirect("http//localhost:5000", 302)  pour rediriger
        headers = {"Content-type": "text/html"}
        return make_response(render_template("confirmation_page.html", email = user.email), 200, headers)
    
    @customer_required
    def set_password(self, user_data:dict):
        
        curent_user_id = get_jwt_identity()
        user = self.user_repository.get_user_by_id(curent_user_id)
        
        # print(user)
        # if not user:
        #     return {"message": "user not found"}, 404
        
        user.password = pbkdf2_sha256.hash(user_data["password"]) 
        # user.is_activated = True
        self.user_repository.save(user)
        self.user_repository.commit()

        return user, 201