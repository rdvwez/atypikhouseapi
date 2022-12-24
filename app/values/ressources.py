from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required

from app.values.models import ValueModel
from app.values.service import ValueService
from schemas import ValueSchema, ValueUpdateSchema, ValueSchema


blp = Blueprint("Values","Value",description="Operations on Values")

@blp.route("/value/<int:value_id>")
class Category(MethodView):

    @inject
    def __init__(self):
        self.value_service = ValueService()

    # @jwt_required()
    @blp.response(200, ValueSchema)
    def get(self, value_id: int):
        return self.value_service.get_value_by_id(value_id) 

    @jwt_required()
    def delete(self, value_id:int):
        return self.value_service.delete_value(value_id)

    #TODO: il faut être connecté et admin pour acceder à cette route
    @jwt_required()
    @blp.arguments(ValueUpdateSchema)
    @blp.response(200, ValueSchema)
    def put(self, value_data, value_id):
        return self.value_service.update_value(value_id= value_id, value_data= value_data)


@blp.route("/value")
class CategoryList(MethodView):

    @inject
    def __init__(self):
        self.value_service = ValueService()


    # @jwt_required()
    @blp.response(200, ValueSchema(many=True))
    def get(self):
        # return "ERT"
        return self.value_service.get_all_values()

    @jwt_required()
    @blp.arguments(ValueSchema)
    @blp.response(200, ValueSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, value_data):
        value = ValueModel(**value_data)
        self.value_service.create_value(value)
        return value
    