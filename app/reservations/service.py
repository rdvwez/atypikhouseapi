import stripe
import os
from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict, Mapping
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from stripe import error

from app.reservations.repository import ReservationRepository
from app.reservations.models import ReservationModel

CURRENCY = "eur"

class ReservationService:

    @inject
    def __init__(self):
         self.reservation_repository = ReservationRepository()


    def get_all_reservations(self)-> List[ReservationModel]:
        """
        Return all reservations
        :return: a list of Reservation objects
        """
        return self.reservation_repository.get_all()

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

    def create_reservation(self, reservation:ReservationModel, strip_token:str):
        """
        Expected for token and a rrservatins data from the request body
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

    def update_reservation(self, reservation_id:int, reservation_data:Dict[str, None]):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            # reservation.show = reservation_data.get("show", 0)
            # reservation.libelle = reservation_data.get("libelle","Not define")
            # self.reservation_repository.save(reservation)
            # self.reservation_repository.commit()
            return reservation
        except:
            abort(404, f"A reservation with id:{reservation_id} doesn't exist")


    def delete_reservation(self, reservation_id):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            self.reservation_repository.delete(reservation)
            self.reservation_repository.commit()
            return  {"message":"reservation deleted"}, 200
        except:
            abort(404, f"A reservation with id:{reservation_id} doesn't exist")
