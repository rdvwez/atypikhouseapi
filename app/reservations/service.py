
import os
import sys
import smtplib
import traceback
import logging
from flask import request, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import stripe
from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict, Mapping, Any
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
    
    def format_reservations_dates(self, reservations: List[ReservationModel]) -> List[ReservationModel]:
        """
        Formate les dates de début et de fin de chaque réservation dans la liste.
        :param reservations: Liste d'objets ReservationModel
        :return: Liste avec les dates formatées
        """
        for reservation in reservations:
            reservation.start_date = reservation.start_date.strftime("%d/%m/%Y")
            reservation.end_date = reservation.end_date.strftime("%d/%m/%Y")
        return reservations
    
    def format_reservation_dates(self, reservation: ReservationModel) -> ReservationModel:
        """
        Formate les dates de début et de fin d'une réservation.
        :param reservation: Objet ReservationModel
        :return: Réservation avec les dates formatées
        """
        reservation.start_date = reservation.start_date.strftime("%d/%m/%Y")
        reservation.end_date = reservation.end_date.strftime("%d/%m/%Y")
        return reservation

    def format_reservation_dates_from_str_to_datetime(self, reservation: ReservationModel) -> ReservationModel:
        """
        Formate les dates de début et de fin d'une réservation de string en dattime.
        :param reservation: Objet ReservationModel
        :return: Réservation avec les dates formatées
        """
        reservation.start_date = datetime.strptime(reservation.start_date, "%d/%m/%Y")
        reservation.end_date = datetime.strptime(reservation.end_date, "%d/%m/%Y")
        return reservation
    
    def format_reservation_dict_dates_from_str_to_datetime(self, reservation_dict:Dict[str, Any]) -> Dict[str, Any]:
        """
        Formate les dates de début et de fin d'une réservation de string en dattime.
        :param reservation: Objet ReservationModel
        :return: Réservation avec les dates formatées
        """
        reservation_dict['start_date'] = datetime.strptime(reservation_dict['start_date'], "%d/%m/%Y")
        reservation_dict['end_date'] = datetime.strptime(reservation_dict['end_date'], "%d/%m/%Y")
        return reservation_dict

    def get_all_reservations(self)-> List[ReservationModel]:
        """
        Return all reservations
        :return: a list of Reservation objects
        """
        reservations = self.reservation_repository.get_all()
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())

        if curent_user.is_owner:
            owner_reservation = [r for r in reservations if
                                 self.houseRepository.get_house_by_id(r.house_id).user_id == curent_user.id]
            return owner_reservation

        elif curent_user.is_customer:
            return [r for r in reservations if r.user_id == curent_user.id]


        return reservations
    
        # reservations  = self.reservation_repository.get_all()
        # curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        
        # if curent_user.is_owner:
        #     owner_reservation = []
        #     for reservation in reservations:
        #         house = self.houseRepository.get_house_by_id(reservation.house_id)
        #         if house.user_id == curent_user.id:
        #             owner_reservation.append(reservation)
        #     return owner_reservation
        
        # elif curent_user.is_customer:
        #     return [reservation for reservation in reservations if reservation.user_id == curent_user.id ]
        
        # return self.reservation_repository.get_all()

    def get_reservation_by_id(self, reservation_id: int) -> ReservationModel:
        # reservation =  self.reservation_repository.get_reservation_by_id(reservation_id)
        return self.reservation_repository.get_reservation_by_id(reservation_id)
    

   
    def initialize_stripe_properties(self, card_number:str, card_exp_month:str, card_exp_year:str, cvc:str, user_email:str):
        payment_methode_id = create_payment_method(card_number = card_number,
                                                card_exp_month = card_exp_month,
                                                card_exp_year = card_exp_year, 
                                                cvc = cvc)

        stripe_customer_id = create_stripe_customer(user_email)
        return payment_methode_id, stripe_customer_id

    def create_reservation(self, reservation_dict:Dict[str, Any]):
        """
        Expected for token and a reservatins data from the request body
        construct an reservation and talk to the strip API to make a charge.
        """
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        house_to_reserve = self.houseRepository.get_house_by_id(reservation_dict['house_id'])

        # reservation_dict['amount'] = house_to_reserve.price * nobre de joure
       
        # logging.error(reservation_dict)
        # reservation = ReservationModel(user_id=curent_user.id, **reservation_dict)
        
        try:
            formated_reservation_dict = self.format_reservation_dict_dates_from_str_to_datetime(reservation_dict)
            difference = formated_reservation_dict['end_date'] - formated_reservation_dict['start_date']
            difference_in_days = difference.days
            formated_reservation_dict['amount'] = house_to_reserve.price * difference_in_days
            # reservation_dict['start_date'] = datetime.strptime(reservation_dict['start_date'], "%d/%m/%Y")
            # reservation_dict['end_date'] = datetime.strptime(reservation_dict['end_date'], "%d/%m/%Y")
            # return start_date
            reservation = ReservationModel(
            user_id=curent_user.id,
            **formated_reservation_dict)
            
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
                # logging.debug(reservation)
                # logging.error(reservation)
                
                return {"message": "reservation failed"}, 500
            else:
                reservation.status = "COMPLETED"
                self.reservation_repository.save(reservation)
                self.reservation_repository.commit()
                # send_email_response = send_reservation_confirmation_mail(email = curent_user.email, subject = "confirmation of your payment", amount = reservation.amount)
        except ValueError as e:
            logging.info('Erreur de conversion de date')
            logging.error(e)
            return {"message": "Erreur de conversion de date"}, 422
        except error.CardError as e:
            logging.info('La carte est expirée, invalide ou si une autre erreur liée à la carte se produit.')
            logging.error(e)
            return e.json_body, e.http_status
        except error.RateLimitError as e:
            logging.info("Cette exception est levée parce que trop d'appels à l'API Stripe en un court laps de temps.")
            logging.error(e)
            return e.json_body, e.http_status
        except error.InvalidRequestError as e:
            logging.info("Données obligatoires manquantes ou indorectes.")
            logging.error(e)
            return e.json_body, e.http_status
        except error.AuthenticationError as e:
            logging.info("Informations d'authentification fournies sont incorrectes ou insuffisantes pour accéder à l'API Stripe")
            logging.error(e)
            return e.json_body, e.http_status 
        except error.StripeError as e:
            logging.error(e)
            return e.json_body, e.http_status
        except Exception as e:
            # logging.debug(reservation)
            logging.info("reservation error")
            logging.error(e)
            return{"message": "reservation error"}, 500
        return reservation, 201

    def update_reservation(self, reservation_id:int, reservation_data:Dict[str, Any]):
        
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)

            # formated_reservation_data = self.format_reservation_dict_dates_from_str_to_datetime(reservation_data)
            
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
