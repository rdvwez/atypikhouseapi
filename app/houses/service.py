from datetime import datetime
from flask import abort 
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from app.houses.repository import HouseRepository
from app.houses.models import HouseModel

class HouseService:

    @inject
    def __init__(self):
         self.house_repository = HouseRepository()

    def get_all_houses(self):
        """
        Return all houses
        :return: a list of House objects
        """
        return self.house_repository.get_all()

    def get_house_by_id(self, house_id: int) -> HouseModel:
        return self.house_repository.get_house_by_id(house_id)


    def create_house(self, house):
        try:
            self.house_repository.save(house)
            self.house_repository.commit()
            return{"message": "house created successfully."}, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the house")

    def update_house(self, house_id:int, house_data:Dict[str, None]):
        try:
            house = self.house_repository.get_house_by_id(house_id)
            house.libelle = house_data.get("libelle", house.libelle)
            house.description = house_data.get("libelle", house.description)
            house.part_number = house_data.get("libelle", house.part_number)
            house.bedroom_number = house_data.get("libelle", house.bedroom_number)
            house.person_number = house_data.get("libelle", house.person_number)
            house.parking_distance = house_data.get("libelle", house.parking_distance)
            house.water = house_data.get("libelle", house.water)
            house.power = house_data.get("libelle", house.power)
            house.price = house_data.get("libelle", house.price)
            house.latitude = house_data.get("libelle", house.latitude)
            house.longitude = house_data.get("libelle", house.longitude)
            house.address = house_data.get("address", house.longitude)
            house.city = house_data.get("city", house.longitude)
            house.country = house_data.get("country", house.longitude)
            
            self.house_repository.save(house)
            self.house_repository.commit()
            # return{"category updated"}, 200
            return house
        except:
            abort(404, f"A house with id:{house_id} doesn't exist")

    def delete_house(self, house_id):
        try:
            house = self.house_repository.get_house_by_id(house_id)
            self.house_repository.delete(house)
            self.house_repository.commit()
            return{"message":"house deleted"}, 200
        except:
            abort(404, f"A category with id:{house_id} doesn't exist")
