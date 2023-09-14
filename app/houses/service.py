from datetime import datetime
from flask import abort 
from typing import List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass

from app.houses.repository import HouseRepository
from app.research.service import ResearchService
from app.houses.models import HouseModel

@dataclass
class Filters:
    category_id: int
    thematic_id: int
    city: str

class HouseService:

    @inject
    def __init__(self):
         self.house_repository = HouseRepository()
         self.research_service = ResearchService()

    def get_all_houses(self):
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
    
    def filter_houses(self, filters: Filters):
        houses = self.house_repository.get_all()

        cat_sorted_houses = self.research_service.sort_houses_by_category_id(houses=houses, category_id=filters.category_id)

        cat_them_sorted_houses = self.research_service.sort_houses_by_thematic_id(houses=cat_sorted_houses, thematic_id=filters.thematic_id)
        
        cat_them_houses_sortd_by_city = [house for house in cat_them_sorted_houses if house.city == filters.city]

        return cat_them_houses_sortd_by_city

