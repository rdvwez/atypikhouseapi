# from sqlalchemy import (Table, Column, Integer, String, )
from datetime import datetime
from flask import abort 
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity

from app.thematics.repository import ThematicRepository
from app.houses.models import HouseModel
from app.thematics.models import ThematicModel
from app.users.repository import UserRepository


class ThematicService:

    @inject
    def __init__(self):
        self.thematic_repository = ThematicRepository()
        self.user_repository = UserRepository()


    def get_all(self):
        """
        Return all categories
        :return: a list of thematic objects
        """
        return self.thematic_repository.get_all()

    def get_thematic_by_id(self, thematic_id):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            return self.thematic_repository.get_thematic_by_id(thematic_id)
        return{"message": "Access Denied"}, 403


    def create_thematic(self, thematic):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            try:
                self.thematic_repository.save(thematic)
                self.thematic_repository.commit()
                return thematic, 201
            except SQLAlchemyError:
                abort(500,"An error occurred while inserting the thematic")
        return{"message": "Access Denied"}, 403

    def update_thematic(self, thematic_id:int, thematic_data:Dict[str, None]):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:
            try:
                thematic = self.thematic_repository.get_thematic_by_id(thematic_id)
                thematic.show = thematic_data.get("show", 0)
                thematic.libelle = thematic_data.get("libelle","Not define")
                self.thematic_repository.save(thematic)
                self.thematic_repository.commit()
                return thematic
            except:
                abort(404, f"A thematic with id:{thematic_id} doesn't exist")
        return{"message": "Access Denied"}, 403

    def delete_thematic(self, thematic_id):
        curent_user = self.user_repository.get_user_by_id(get_jwt_identity())
        if curent_user.is_admin:    
            try:
                thematic = self.thematic_repository.get_thematic_by_id(thematic_id)
                self.thematic_repository.delete(thematic)
                self.thematic_repository.commit()
                return{"message": "thematic deleted"}, 204
            except:
                abort(404, message=f"A thematic with id:{thematic_id} doesn't exist")
        return{"message": "Access Denied"}, 403

    def get_houses_in_thematic(self, thematic_id:int) -> List[HouseModel]:
        """Get Houses which belong to category

        Args:
            category_id (int): id of the category

        Returns:
            List[HouseModel]: List of Houses
        """
        thematic = self.thematic_repository.get_thematic_by_id(thematic_id)

        return thematic.houses.all()