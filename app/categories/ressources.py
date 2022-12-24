from typing import List, Dict
from flask import request,  jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required

from app.categories.models import CategoryModel
from app.categories.service import CategoryService
from schemas import CategorySchema, CategoryUpdateSchema, HouseSchema


blp = Blueprint("Categories","categories",description="Operations on categories")


@blp.route("/category/<string:category_id>/house")
class HousesInCategory(MethodView):

    @inject
    def __init__(self):
        self.category_service = CategoryService()

    @jwt_required()
    @blp.response(200, HouseSchema(many=True))
    def get(self, category_id:int):
        return self.category_service.get_houses_in_category(category_id) 


@blp.route("/category/<int:category_id>")
class Category(MethodView):

    @inject
    def __init__(self):
        self.category_service = CategoryService()

    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id:int):
        
        return self.category_service.get_category_by_id(category_id) 

    @jwt_required()
    def delete(self, category_id):
        return self.category_service.delete_category(category_id)

    #TODO: il faut être connecté et admin pour acceder à cette route
    @jwt_required(fresh=True)
    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, CategorySchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    # def put(self, *args, **kwargs):
    def put(self, category_data, category_id):
        
    #    return self.category_service.update_category(kwargs["category_id"], args[0])
       return self.category_service.update_category(category_id= category_id, category_data= category_data)
        


@blp.route("/category")
class CategoryList(MethodView):

    @inject
    def __init__(self):
        self.category_service = CategoryService()

    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return self.category_service.get_all_categories()

    # @jwt_required(fresh=True)
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    # category_data contain the json wich is the validated fileds that the schamas requested
    def post(self, category_data:Dict[str, None]):
        category = CategoryModel(**category_data)
        # print(category)
        # category = CategoryModel(libelle = category_data.get("libelle", "Not Define"), show = category_data.get("libelle", "Not define"))
        self.category_service.create_category(category)
        return category
    