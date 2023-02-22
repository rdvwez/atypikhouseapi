from datetime import datetime
from flask import abort, jsonify
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from app.categories.repository import CategoryRepository
from app.houses.models import HouseModel
from app.categories.models import CategoryModel


class CategoryService:

    @inject
    def __init__(self):
         self.category_repository = CategoryRepository()


    def get_all_categories(self)-> List[CategoryModel]:
        """
        Return all categories
        :return: a list of Category objects
        """
        return self.category_repository.get_all()

    def get_category_by_id(self, category_id: int) -> CategoryModel:
        # return self.category_repository.get_category_by_id(category_id)
        return self.category_repository.get_category_by_id(category_id)


    def create_category(self, category):
        try:
            # print(category)
            self.category_repository.save(category)
            self.category_repository.commit()
            
            return{"message": "category created successfully."}, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the category")

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


    def delete_category(self, category_id):
        try:
            category = self.category_repository.get_category_by_id(category_id)
            self.category_repository.delete(category)
            self.category_repository.commit()
            return  {"message":"category deleted"}, 200
        except:
            abort(404, f"A category with id:{category_id} doesn't exist")

    def get_houses_in_category(self, category_id:int) -> List[HouseModel]:
        """Get Houses which belong to category

        Args:
            category_id (int): id of the category

        Returns:
            List[HouseModel]: List of Houses
        """
        category = self.category_repository.get_category_by_id(category_id)

        return category.houses.all()