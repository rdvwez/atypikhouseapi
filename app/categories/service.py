import json
from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict, Mapping
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity

from app.categories.repository import CategoryRepository
from app.houses.models import HouseModel
from app.categories.models import CategoryModel
from app.users.repository import UserRepository
from app.libs.decorators import admin_required


class CategoryService:

    @inject
    def __init__(self):
        self.category_repository = CategoryRepository()
        self.user_repository = UserRepository()


    def get_all_categories(self):
        """
        Return all categories
        :return: a list of Category objects
        """
        
        return self.category_repository.get_all()

    @admin_required
    def get_category_by_id(self, category_id: int) -> CategoryModel :
        return self.category_repository.get_category_by_id(category_id)
        

    @admin_required
    def create_category(self, category):
        try:
            self.category_repository.save(category)
            self.category_repository.commit()
            return category, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the category")

    @admin_required
    def update_category(self, category_id:int, category_data:Dict[str, None]):
        try:
            category = self.category_repository.get_category_by_id(category_id)
            category.show = category_data.get("show", 0)
            category.libelle = category_data.get("libelle","Not define")
            self.category_repository.save(category)
            self.category_repository.commit()
            return category
        except:
            abort(404, f"A category with id:{category_id} doesn't exist")

    @admin_required
    def delete_category(self, category_id):
        try:
            category = self.category_repository.get_category_by_id(category_id)
            self.category_repository.delete(category)
            self.category_repository.commit()
            return  {"message":"category deleted"}, 204
        except:
            abort(404, f"A category with id:{category_id} doesn't exist")

    @admin_required
    def get_houses_in_category(self, category_id:int) -> List[HouseModel]:
        """Get Houses which belong to category

        Args:
            category_id (int): id of the category

        Returns:
            List[HouseModel]: List of Houses
        """
        category = self.category_repository.get_category_by_id(category_id)

        return category.houses.all()