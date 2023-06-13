import stripe
import os
from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict, Mapping
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from stripe import error
from flask_jwt_extended import get_jwt_identity

from app.reservations.repository import ReservationRepository
from app.reservations.models import ReservationModel
from app.libs.decorators import owner_required, admin_required, customer_required
from app.users.repository import UserRepository
from app.houses.repository import HouseRepository

CURRENCY = "eur"

class ReservationService:

    @inject
    def __init__(self):
         self.reservation_repository = ReservationRepository()
         self.user_repository = UserRepository()
         self.houseRepository = HouseRepository()

    @customer_required
    def get_all_reservations(self)-> List[ReservationModel]:
        """
        Return all reservations
        :return: a list of Reservation objects
        """
    
        reservations  = self.reservation_repository.get_all()
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_customer:
            return [reservation for reservation in reservations if reservation.user_id == curent_user.id ]
            
        elif curent_user.is_owner:
            owner_reservation = []
            for reservation in reservations:
                house = self.houseRepository.get_house_by_id(reservation.house_id)
                if house.user_id == curent_user.id:
                    owner_reservation.append(reservation)
            return owner_reservation 
        
        return self.reservation_repository.get_all()

    @customer_required
    def get_reservation_by_id(self, reservation_id: int) -> ReservationModel:
        # return self.reservation_repository.get_reservation_by_id(reservation_id)
        return self.reservation_repository.get_reservation_by_id(reservation_id)

    def charge_with_stripe(self, strip_token: str, amount:float,  description:str)-> stripe.Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        return stripe.Charge.create(
            amount= amount, # amount of cents(100 means USD$1.00)
            currency= CURRENCY,
            description= description,
            source= strip_token
        )

    @customer_required
    def create_reservation(self, reservation:ReservationModel, strip_token:str):
        """
        Expected for token and a reservatins data from the request body
        construct an reservation and talk to the strip API to make a charge.
        """
        try:
            # reservation.amount = (reservation.end_date - reservation.start_date).days
            self.reservation_repository.save(reservation)
            self.reservation_repository.commit()
            description = f"This reservation costs {reservation.amount}, starts {reservation.start_date} an ends {reservation.end_date} "
            try:
                reservation.status = "failed"
                self.charge_with_stripe(strip_token, reservation.amount, description)
                reservation.status = "complete"
            except error.CardError as e:
                return e.json_body, e.http_status
            except error.RateLimitError as e:
                return e.json_body, e.http_status
            except error.InvalidRequestError as e:
                return e.json_body, e.http_status
            except error.AuthenticationError as e:
                return e.json_body, e.http_status 
            except error.StripeError as e:
                return e.json_body, e.http_status
            except Exception as e:
                print(e)
                return{"message": "reservation error"}, 500
            return{"message": "reservation saved successfully."}, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the reservation")

    @owner_required
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

    @owner_required
    def delete_reservation(self, reservation_id):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            self.reservation_repository.delete(reservation)
            self.reservation_repository.commit()
            return  {"message":"reservation deleted"}, 204
        except:
            abort(404, f"A reservation with id:{reservation_id} doesn't exist")
