from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject
from flask_jwt_extended import jwt_required


from schemas import CityListchema, HouseSchema, HouseUpdateSchema, HouseCitiesSchema, HouseFilterSchema, HouseLimitedSchemaForResearch, HouseWithPropertiesSchema
from app.houses.service import HouseService
from app.houses.models import HouseModel
from app.libs.decorators import owner_required
from app.houses.service import Filters

blp = Blueprint("Houses",__name__,description="Operations on houses",url_prefix="/api")

@blp.route("/house/<string:house_id>")
class House(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    # @jwt_required()
    # @owner_required
    @blp.response(200, HouseWithPropertiesSchema)
    @blp.doc(tags=['Houses'], security=[{}])
    def get(self, house_id:int):
        """Find houses by ID

        Return houses based on ID.
        ---
        Internal comment not meant to be exposed.
        """
        return self.house_service.get_house_by_id(house_id) 

    @jwt_required()
    @owner_required
    @blp.doc(tags=['Houses'], security=[{'Bearer': []}])
    def delete(self, house_id:int):
        return self.house_service.delete_house(house_id)

    @jwt_required(fresh=True)
    @owner_required
    @blp.arguments(HouseUpdateSchema) 
    @blp.response(200, HouseSchema)
    @blp.doc(tags=['Houses'], security=[{'Bearer': []}])
    def put(self, house_data, house_id):
        return self.house_service.update_house(house_id= house_id, house_data= house_data)


@blp.route("/house")
class HouseList(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.doc(tags=['Houses'], security=[{}])
    @blp.response(200, HouseWithPropertiesSchema(many=True))
    def get(self):
        return self.house_service.get_all_houses()

    @jwt_required()
    @owner_required
    @blp.arguments(HouseSchema)
    @blp.response(201, HouseSchema)
    @blp.doc(tags=['Houses'], security=[{'Bearer': []}])
    def post(self, house_data):
        house = HouseModel(**house_data)
        return self.house_service.create_house(house)
    
@blp.route("/house/byuserprofile")
class HouseListByUserProfiled(MethodView):

    @inject
    def __init__(self):
        self.house_service = HouseService()

    @jwt_required()
    @owner_required
    @blp.doc(tags=['Houses'], security=[{'Bearer': []}])
    @blp.response(200, HouseWithPropertiesSchema(many=True))
    def get(self):
        """
        Returns houses by user profile 
        """
        return self.house_service.get_houses_by_user_profile()
    
@blp.route("/house/cities")
class CityList(MethodView):
    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.doc(tags=['Houses'], security=[{}])
    @blp.response(200, CityListchema(many=True))
    def get(self):

        """
        Returns list of city houses 
        """
        cities = self.house_service.get_cities_with_photos()
        return cities
    
@blp.route("/house/filter")
class HouseFilter(MethodView):
    @inject
    def __init__(self):
        self.house_service = HouseService()

    @blp.arguments(HouseFilterSchema)
    @blp.response(201, HouseWithPropertiesSchema(many=True))
    @blp.doc(tags=['Houses'], security=[{'Bearer': []}])
    def post(self, filter_data):
        filters = Filters(category_id= filter_data.get("category_id", None),
                          thematic_id=filter_data.get("thematic_id", None),
                          city= filter_data.get("city", None))
        return self.house_service.filter_houses(filters)