from datetime import datetime
from flask import abort 
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass
from flask_jwt_extended import get_jwt_identity

from app.houses.repository import HouseRepository
from app.research.service import ResearchService
from app.houses.models import HouseModel

@dataclass
class Filters:
    category_id: int | None
    thematic_id: int | None
    city: str | None

class HouseService:

    @inject
    def __init__(self):
         self.house_repository = HouseRepository()
         self.research_service = ResearchService()

    def get_all_houses(self) -> List[HouseModel]:
        """
        Return all houses
        :return: a list of House objects
        """
        return self.house_repository.get_all()
 
    def get_house_by_id(self, house_id: int) -> HouseModel:
        return self.house_repository.get_house_by_id(house_id)

    def create_house(self, house:HouseModel):
        try:
            self.house_repository.save(house)
            self.house_repository.commit()
            return house, 201
        except SQLAlchemyError:
            abort(500,"An error occurred while inserting the house")

    def update_house(self, house_id:int, house_data:Dict[str, None]):
        try:
            
            house = self.house_repository.get_house_by_id(house_id)
            house.libelle = house_data.get("libelle", house.libelle)
            house.description = house_data.get("description", house.description)
            house.bedroom_number = house_data.get("bedroom_number", house.bedroom_number)
            house.person_number = house_data.get("person_number", house.person_number)
            house.parking_distance = house_data.get("parking_distance", house.parking_distance)
            house.water = house_data.get("water", house.water)
            house.power = house_data.get("power", house.power)
            house.price = house_data.get("price", house.price)
            house.latitude = house_data.get("latitude", house.latitude)
            house.longitude = house_data.get("longitude", house.longitude)
            house.address = house_data.get("address", house.address)
            house.city = house_data.get("city", house.city)
            house.country = house_data.get("country", house.country)
            
            self.house_repository.save(house)
            self.house_repository.commit()
            
            return house
        except:
            abort(404, f"A house with id:{house_id} doesn't exist")

    def delete_house(self, house_id:int):
        try:
            house = self.house_repository.get_house_by_id(house_id)
            self.house_repository.delete(house)
            self.house_repository.commit()
    
            return{"message":"house deleted"}, 204
        except:
            abort(404, f"A category with id:{house_id} doesn't exist")

    
    def filter_houses(self, filters: Filters) ->  List[HouseModel]:
        houses = self.house_repository.get_all()

        filtered_houses = [house for house in houses if
                           ( filters.category_id is None or house.category_id == filters.category_id) and
                           ( filters.thematic_id is None or house.thematic_id == filters.thematic_id) and
                           ( filters.city is None or house.city == filters.city)]

        return filtered_houses
    
    def get_houses_by_user_profile(self) -> List[HouseModel]:
        curent_user_id = get_jwt_identity()
        houses = self.get_all_houses()

        return [house for house in houses if house.user_id == curent_user_id ]

