from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required
# from injector import inject
# from service import CategoryService

from app.properties.models import PropertyModel
from app.properties.service import PropertyService
from schemas import PropertySchema, PropertyUpdateSchema, HouseSchema


blp = Blueprint("Properties",__name__,description="Operations on Properties")


@blp.route("/property/<int:property_id>")
class Property(MethodView):

    @inject
    def __init__(self):
        self.property_service = PropertyService()

    # @jwt_required()
    @blp.response(200, PropertySchema)
    def get(self, property_id):
        return self.property_service.get_property_by_id(property_id) 

    @jwt_required()
    def delete(self, property_id):
        return self.property_service.delete_property(property_id)

    #TODO: il faut être connecté et admin pour acceder à cette route
    @jwt_required()
    @blp.arguments(PropertyUpdateSchema)
    @blp.response(200, PropertySchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def put(self, property_data, property_id):
         return self.property_service.update_property(property_id= property_id, property_data= property_data)


@blp.route("/property")
class PropertyList(MethodView):

    @inject
    def __init__(self):
        self.property_service = PropertyService()


    # @jwt_required()
    @blp.response(200, PropertySchema(many=True))
    def get(self):
        # return "ERT"
        return self.property_service.get_all_properties()

    @jwt_required()
    @blp.arguments(PropertySchema)
    @blp.response(200, PropertySchema)
    # property_data contain the json wich is the validated fileds that the schamas requested
    def post(self, property_data):
        property_object = PropertyModel(**property_data)
        self.property_service.create_property(property_object)
        return property_object
    