
import os
import sys
import smtplib
import traceback
from flask import request, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import stripe
from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict, Mapping
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from stripe import error

from flask_jwt_extended import get_jwt_identity
from app.users.repository import UserRepository

from app.reservations.repository import ReservationRepository
from app.reservations.models import ReservationModel
from app.users.repository import UserRepository
from app.houses.repository import HouseRepository
from app.libs.stripe_helper import create_payment_method, create_stripe_customer, attach_paymentmethod_to_customer, create_subscription
from app.libs.email_sender import send_reservation_confirmation_mail

CURRENCY = "eur"


class ReservationService:

    @inject
    def __init__(self):
         self.reservation_repository = ReservationRepository()
         self.user_repository = UserRepository()
         self.houseRepository = HouseRepository()

    def get_all_reservations(self)-> List[ReservationModel]:
        """
        Return all reservations
        :return: a list of Reservation objects
        """
    
        reservations  = self.reservation_repository.get_all()
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        
        if curent_user.is_owner:
            owner_reservation = []
            for reservation in reservations:
                house = self.houseRepository.get_house_by_id(reservation.house_id)
                if house.user_id == curent_user.id:
                    owner_reservation.append(reservation)
            return owner_reservation
        
        elif curent_user.is_customer:
            return [reservation for reservation in reservations if reservation.user_id == curent_user.id ]
        
        return self.reservation_repository.get_all()

    def get_reservation_by_id(self, reservation_id: int) -> ReservationModel:
        return self.reservation_repository.get_reservation_by_id(reservation_id)
    

   
    def initialize_stripe_properties(self, card_number:str, card_exp_month:str, card_exp_year:str, cvc:str, user_email:str):
        payment_methode_id = create_payment_method(card_number = card_number,
                                                card_exp_month = card_exp_month,
                                                card_exp_year = card_exp_year, 
                                                cvc = cvc)

        stripe_customer_id = create_stripe_customer(user_email)
        return payment_methode_id, stripe_customer_id

    def create_reservation(self, reservation:ReservationModel):
        """
        Expected for token and a reservatins data from the request body
        construct an reservation and talk to the strip API to make a charge.
        """
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())

        try:
            
            if not curent_user.payment_methode and not curent_user.stripe_custome_id:
                
                payment_methode_id, stripe_customer_id = self.initialize_stripe_properties(
                                                                card_number = reservation.card_number,
                                                                card_exp_month = reservation.card_exp_month,
                                                                card_exp_year = reservation.card_exp_year, 
                                                                cvc = reservation.cvc,
                                                                user_email = curent_user.email
                                                                )
                
                payment_methode_attached = attach_paymentmethod_to_customer(payment_methode_id, stripe_customer_id )
                
                curent_user.payment_methode = payment_methode_id
                curent_user.stripe_custome_id = stripe_customer_id
   
            subscription = create_subscription(curent_user.stripe_custome_id, curent_user.payment_methode)
            
            if not subscription:
                reservation.status = "FAILED"
                return {"message": "reservation failed"}, 500
            else:
                reservation.status = "COMPLETED"
                self.reservation_repository.save(reservation)
                self.reservation_repository.commit()
                # send_email_response = send_reservation_confirmation_mail(email = curent_user.email, subject = "confirmation of your payment", amount = reservation.amount)

        except error.CardError as e:
            print("La carte est expirée, invalide ou si une autre erreur liée à la carte se produit.")
            return e.json_body, e.http_status
        except error.RateLimitError as e:
            print("Cette exception est levée parce que trop d'appels à l'API Stripe en un court laps de temps.")
            return e.json_body, e.http_status
        except error.InvalidRequestError as e:
            print("Données obligatoires manquantes ou indorectes.")
            return e.json_body, e.http_status
        except error.AuthenticationError as e:
            print("Informations d'authentification fournies sont incorrectes ou insuffisantes pour accéder à l'API Stripe")
            return e.json_body, e.http_status 
        except error.StripeError as e:
            return e.json_body, e.http_status
        except Exception as e:
            print(e)
            return{"message": "reservation error"}, 500
        return reservation, 201

    def update_reservation(self, reservation_id:int, reservation_data:Dict[str, None]):
        
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            
            reservation.end_date = reservation_data.get("end_date")
            reservation.start_date = reservation_data.get("start_date")
            reservation.status = reservation_data.get("status").value

            self.reservation_repository.save(reservation)
            self.reservation_repository.commit()
            return reservation,200
        except Exception as err:
            abort(404, f"A reservation with id:{reservation_id} doesn't exist")

    def delete_reservation(self, reservation_id):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            self.reservation_repository.delete(reservation)
            self.reservation_repository.commit()
            return  {"message":"reservation deleted"}, 204
        except:
            abort(404, f"A reservation with id:{reservation_id} doesn't exist")
