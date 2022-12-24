from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject

from schemas import HouseSchema, HouseUpdateSchema
from app.houses.service import HouseService
from app.houses.models import HouseModel




blp = Blueprint("Houses",__name__,description="Operations on houses")




@blp.route("/house/<string:house_id>")
class Category(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.response(200, HouseSchema)
    def get(self, house_id:int):
        return self.house_service.get_house_by_id(house_id) 


    def delete(self, house_id:int):
        return self.house_service.delete_house(house_id)

    @blp.arguments(HouseUpdateSchema) 
    @blp.response(200, HouseSchema)
    # house_data contain the json wich is the validated fileds that the schamas requested
    def put(self, house_data, house_id):
        return self.house_service.update_house(house_id= house_id, house_data= house_data)


@blp.route("/house")
class CategoryList(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.response(200, HouseSchema(many=True))
    def get(self):
        return self.house_service.get_all_houses()

    @blp.arguments(HouseSchema)
    @blp.response(200, HouseSchema)
    # house_data contain the json wich is the validated fileds that the schamas requested
    def post(self, house_data):
        house = HouseModel(**house_data)
        self.house_service.create_house(house)
        return house