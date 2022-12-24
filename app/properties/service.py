from datetime import datetime
from flask import abort 
from typing import List, Dict, Tuple, Literal
from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from app.properties.repository import PropertyRepository
from app.properties.models import PropertyModel


class PropertyService:

    @inject
    def __init__(self):
         self.property_repository = PropertyRepository()


    def get_all_properties(self):
        """
        Return all properties
        :return: a list of Prperty objects
        """
        return self.property_repository.get_all()

    def get_property_by_id(self, property_id):
        # return self.category_repository.get_category_by_id(category_id)
        return self.property_repository.get_property_by_id(property_id)


    def create_property(self, property_object:PropertyModel)-> Tuple[Dict[str, str], Literal[201]]:
        try:
            self.property_repository.save(property_object)
            self.property_repository.commit()
            return{"message": "property created successfully."}, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the property")

    def update_property(self, property_id:int, property_data:Dict[str, None]):
        try:
            property_object = self.property_repository.get_property_by_id(property_id)
            property_object.libelle= property_data.get("libelle", "Not define")
            property_object.description = property_data.get("description","Not define")
            self.property_repository.save(property_object)
            self.property_repository.commit()
            return property_object
        except:
            abort(404, f"A property with id:{property_id} doesn't exist")

    def delete_property(self, property_id):
        try:
            property_object = self.property_repository.get_property_by_id(property_id)
            self.property_repository.delete(property_object)
            self.property_repository.commit()
            return{"message": "property deleted"}, 200
        except:
            abort(404, message=f"A property with id:{property_id} doesn't exist")

    # def get_houses_in_category(self, category_id:int) -> List[HouseModel]:
    #     """Get Houses which belong to category

    #     Args:
    #         category_id (int): id of the category

    #     Returns:
    #         List[HouseModel]: List of Houses
    #     """
    #     cateegory = self.category_repository.get_category_by_id(category_id)

    #     return cateegory.houses.all()