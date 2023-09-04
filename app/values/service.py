# from sqlalchemy import (Table, Column, Integer, String, )
from datetime import datetime
from flask import abort 
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity

from app.values.repository import ValueRepository
from app.users.repository import UserRepository



class ValueService:

    @inject
    def __init__(self):
         self.value_repository = ValueRepository()
         self.user_repository = UserRepository()


    def get_all_values(self):
        """
        Return all values
        :return: a list of Values
        """
        curent_user_id = get_jwt_identity()
        values = self.value_repository.get_all()
        current_user_values = [value for value in values if value.user_id == curent_user_id]
        return current_user_values

    def get_value_by_id(self, value_id):
            return self.value_repository.get_value_by_id(value_id)

    def create_value(self, value):
        try:
            self.value_repository.save(value)
            self.value_repository.commit()
            return value, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the value")

    def update_value(self, value_id:int, value_data:Dict[str, None]):
        try:
            value = self.value_repository.get_value_by_id(value_id)
            
            value.libelle = value_data.get("libelle", "Not define")
            self.value_repository.save(value)
            self.value_repository.commit()
            return value
        except:
            abort(404, f"A value with id:{value_id} doesn't exist")

    def delete_value(self, value_id:int):
        try:
            value = self.value_repository.get_value_by_id(value_id)
            self.value_repository.delete(value)
            self.value_repository.commit()
            return{"message": "value deleted"}, 204
        except:
            abort(404, message=f"A value with id:{value_id} doesn't exist")
