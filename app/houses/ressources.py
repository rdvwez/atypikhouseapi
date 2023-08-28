from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort, requires, doc
from injector import inject
from flask_jwt_extended import jwt_required


from schemas import HouseSchema, HouseUpdateSchema, HouseCitiesSchema
from app.houses.service import HouseService
from app.houses.models import HouseModel




blp = Blueprint("Houses",__name__,description="Operations on houses",url_prefix="/api")




@blp.route("/house/<string:house_id>")
class Category(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    @jwt_required()
    @requires("Authorization", description="Authentication token required")
    @blp.response(200, HouseSchema)
    @doc(tags=['Houses'], security=[{'Bearer': []}])
    def get(self, house_id:int):
        return self.house_service.get_house_by_id(house_id) 

    @jwt_required()
    @requires("Authorization", description="Authentication token required")
    @doc(tags=['Houses'], security=[{'Bearer': []}])
    def delete(self, house_id:int):
        return self.house_service.delete_house(house_id)

    @jwt_required(fresh=True)
    @requires("Authorization", description="Authentication token required")
    @blp.arguments(HouseUpdateSchema) 
    @blp.response(200, HouseSchema)
    @doc(tags=['Houses'], security=[{'Bearer': []}])
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

    @jwt_required()
    @requires("Authorization", description="Authentication token required")
    @blp.arguments(HouseSchema)
    @blp.response(201, HouseSchema)
    @doc(tags=['Houses'], security=[{'Bearer': []}])
    def post(self, house_data):
        house = HouseModel(**house_data)
        return self.house_service.create_house(house)
    
@blp.route("/house/cities")
class CityList(MethodView):
    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.response(200, HouseCitiesSchema(many=True))
    def get(self):

        """
        Returns list of city houses 
        """
        cities = [ house.city for house in self.house_service.get_all_houses()]
        return cities