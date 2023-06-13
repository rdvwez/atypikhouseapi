from typing import List, Dict, Mapping
from flask import request,  jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required

from app.reservations.models import ReservationModel
from app.reservations.service import ReservationService
from schemas import ReservationSchema, ReservationUpdateSchema


blp = Blueprint("Reservations","reservations",description="Operations on reservations", url_prefix="/api")


# @blp.route("/category/<string:category_id>/house")
# class HousesInCategory(MethodView):

#     @inject
#     def __init__(self):
#         self.category_service = CategoryService()

#     @jwt_required()
#     @blp.response(200, HouseSchema(many=True))
#     def get(self, category_id:int):
#         return self.category_service.get_houses_in_category(category_id) 


@blp.route("/reservation/<int:reservation_id>")
class Reservation(MethodView):

    @inject
    def __init__(self):
        self.reservation_service = ReservationService()

    @jwt_required()
    @blp.response(200, ReservationSchema)
    def get(self, reservation_id:int):
        return self.reservation_service.get_reservation_by_id(reservation_id) 

    @jwt_required()
    def delete(self, reservation_id):
        return self.reservation_service.delete_reservation(reservation_id)

    #TODO: il faut être connecté et admin pour acceder à cette route
    @jwt_required(fresh=True)
    @blp.arguments(ReservationUpdateSchema)
    @blp.response(200, ReservationSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def put(self, *args, **kwargs):
        return self.reservation_service.update_reservation(kwargs["reservation_id"], args[0])
        


@blp.route("/reservation")
class ReservationList(MethodView):

    @inject
    def __init__(self):
        self.reservation_service = ReservationService()

    @jwt_required()
    @blp.response(200, ReservationSchema(many=True))
    def get(self):
        return self.reservation_service.get_all_reservations()

        
    @jwt_required(fresh=True)
    @blp.arguments(ReservationSchema)
    @blp.response(200, ReservationSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, data:Mapping[str, Mapping]):
        """
        Expected for token and a reservations data from the request body
        construct a reservation and talk to the strip API to make a charge.
        """
        reservation = ReservationModel(**data["reservation_data"])
        # print(category)
        # category = CategoryModel(libelle = category_data.get("libelle", "Not Define"), show = category_data.get("libelle", "Not define"))
        self.reservation_service.create_reservation(reservation, data.get("strip_token"))
        return reservation
    