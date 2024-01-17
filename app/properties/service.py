from datetime import datetime
from flask import abort 
from typing import List, Dict, Tuple, Literal
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity

from app.properties.repository import PropertyRepository
from app.properties.models import PropertyModel
from app.users.repository import UserRepository


class PropertyService:

    @inject
    def __init__(self):
        self.property_repository = PropertyRepository()
        self.user_repository = UserRepository()


    def get_all_properties(self):
        """
        Return all properties
        :return: a list of Prperty objects
        """
        return self.property_repository.get_all()

    def get_property_by_id(self, property_id):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            return self.property_repository.get_property_by_id(property_id)
        return{"message": "Access Denied"}, 403


    def create_property(self, property_object:PropertyModel):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            try:
                self.property_repository.save(property_object)
                self.property_repository.commit()
                return property_object, 201
            except SQLAlchemyError:
                abort(500,"An error occurred while inserting the property")
        return{"message": "Access Denied"}, 403

    def update_property(self, property_id:int, property_data:Dict[str, None]):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            try:
                property_object = self.property_repository.get_property_by_id(property_id)
                property_object.libelle= property_data.get("libelle", "Not define")
                property_object.category_id= property_data.get("category_id", "Not define")
                property_object.description = property_data.get("description","Not define")
                self.property_repository.save(property_object)
                self.property_repository.commit()
                return property_object
            except:
                abort(404, f"A property with id:{property_id} doesn't exist")
        return{"message": "Access Denied"}, 403

    def delete_property(self, property_id):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            try:
                property_object = self.property_repository.get_property_by_id(property_id)
                self.property_repository.delete(property_object)
                self.property_repository.commit()
                return{"message": "property deleted"}, 200
            except:
                abort(404, message=f"A property with id:{property_id} doesn't exist")
        return{"message": "Access Denied"}, 403
    
    def get_properties_by_category_id(self, category_id:int)->List[PropertyModel]:
        category_properties = self.property_repository.get_properties_by_category_id(category_id)
        return category_properties