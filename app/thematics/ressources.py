from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required
# from injector import inject
# from service import CategoryService

from app.thematics.models import ThematicModel
from app.thematics.service import ThematicService
from schemas import ThematicSchema, ThematicUpdateSchema, HouseSchema
from app.libs.decorators import admin_required



blp = Blueprint("Thematics","thematics",description="Operations on thematics",url_prefix="/api")


@blp.route("/thematic/<string:thematic_id>/house")
class HousesInThematic(MethodView):

    @inject
    def __init__(self):
        self.thematic_service = ThematicService()

    @jwt_required()
    @admin_required
    @blp.response(200, HouseSchema(many=True))
    def get(self, thematic_id):
        return self.thematic_service.get_houses_in_thematic(thematic_id) 


@blp.route("/thematic/<int:thematic_id>")
class Category(MethodView):

    @inject
    def __init__(self):
        self.thematic_service = ThematicService()

    @jwt_required()
    @admin_required
    @blp.response(200, ThematicSchema)
    def get(self, thematic_id:int):
        return self.thematic_service.get_thematic_by_id(thematic_id) 

    @jwt_required()
    @admin_required
    def delete(self, thematic_id:int):
        return self.thematic_service.delete_thematic(thematic_id)

    #TODO: il faut être connecté et admin pour acceder à cette route
    @jwt_required(fresh=True)
    @admin_required
    @blp.arguments(ThematicUpdateSchema)
    @blp.response(200, ThematicSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def put(self, thematic_data, thematic_id):
        return self.thematic_service.update_thematic(thematic_id= thematic_id, thematic_data= thematic_data)


@blp.route("/thematic")
class ThematicList(MethodView):

    @inject
    def __init__(self):
        self.thematic_service = ThematicService()


    @blp.response(200, ThematicSchema(many=True))
    @blp.doc(tags=['Thematics'], security=[{}])
    def get(self):
        return self.thematic_service.get_all()

    @jwt_required(fresh=True)
    @admin_required
    @blp.arguments(ThematicSchema)
    @blp.response(201, ThematicSchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, thematic_data):
        thematic = ThematicModel(**thematic_data)
        return self.thematic_service.create_thematic(thematic)
        
    