import default_config as dc
import logging
import os
from datetime import datetime
import random
import requests
from flask import abort 
from typing import Any, List, Dict
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass
from flask_jwt_extended import get_jwt_identity

from app.houses.repository import HouseRepository
from app.research.service import ResearchService
from app.houses.models import HouseModel
from app.properties.service import PropertyService
from app.properties.models import PropertyModel
from app.values.service import ValueService
from app.images.models import ImageModel

@dataclass
class Filters:
    category_id: int | None
    thematic_id: int | None
    city: str | None

SEARCH_PARAMS = {'query': 'city', 'client_id': os.environ.get('UNSPLASH_ACCESS_KEY')}

class HouseService:

    @inject
    def __init__(self):
         self.house_repository = HouseRepository()
         self.research_service = ResearchService()
         self.property_service = PropertyService()
         self.value_service = ValueService()

    def get_value_label(self, property_id: int, user_id: int)->str:
        value_model = self.value_service.get_value_by_property_id_and_user_id(user_id=user_id, property_id=property_id)
        
        if value_model is not None:
            return value_model.libelle
        else:
            # Gérer le cas où la valeur est None, peut-être en renvoyant une valeur par défaut
            return "Non pas disponible pour cette hébergement"
    def match_properety_to_value(self, properties:List[PropertyModel], user_id:int)->List[dict[str, str]]:
        return [
            {
                "libelle":p.libelle,
                "value": self.get_value_label(p.id, user_id)
            } 
            for p in properties]
    def reformat_images(self,images: List[ImageModel], category:str)->List[Dict[str, str]]:
        return [{
            "path":image.path,
            "category": category
        } for image in images]
    
    def dictionarize_house_with_properties(self,house:HouseModel)  -> dict[str, Any]:
        return {
                "id" : house.id,
                "libelle" : house.libelle,
                "description" : house.libelle,
                "bedroom_number" : house.bedroom_number,
                "person_number" : house.person_number,
                "parking_distance" : house.parking_distance,
                "area" : house.area,
                "water" : house.water,
                "power" : house.power,
                "price" : house.price,
                "latitude" : house.latitude,
                "longitude" : house.longitude,
                "address" : house.address,
                "city" : house.city,
                "country" : house.country,
                "created_at" : house.created_at,
                "category_id" :house.category_id,
                "thematic_id" : house.thematic_id,
                "category": house.category,
                "thematic": house.thematic,
                "images":house.images,
                "properties":self.match_properety_to_value(
                                            properties=self.property_service.get_properties_by_category_id(house.category_id),
                                            user_id = house.user_id)
            }
        
    def add_properties_houses(self, houses:List[HouseModel]):
        return [ self.dictionarize_house_with_properties(house=house) for house in houses ]

    def get_all_houses(self) ->List[Dict[str, Any]]:
        """
        Return all houses
        :return: a list of House objects
        """
        houses = self.house_repository.get_all()
        houses_with_properties = self.add_properties_houses(houses=houses)
        return houses_with_properties
 
    def get_house_by_id(self, house_id: int) ->Dict[str, Any]:
        house = self.house_repository.get_house_by_id(house_id)
        return self.dictionarize_house_with_properties(house=house) 
        

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

    
    def filter_houses(self, filters: Filters) -> List[Dict[str, Any]]:
        houses = self.house_repository.get_all()

        filtered_houses = [house for house in houses if
                           ( filters.category_id is None or house.category_id == filters.category_id) and
                           ( filters.thematic_id is None or house.thematic_id == filters.thematic_id) and
                           ( filters.city is None or house.city == filters.city)]
        filtered_houses_with_properties = self.add_properties_houses(filtered_houses)

        return filtered_houses_with_properties
    
    def get_houses_by_user_profile(self) ->List[Dict[str, Any]]:
        curent_user_id = get_jwt_identity()
        houses = self.house_repository.get_all()
        sorted_houses = [house for house in houses if house.user_id == curent_user_id ]
        houses_with_properties = self.add_properties_houses(sorted_houses)
        return houses_with_properties
    
    def get_photos(self, cities: List[str])->Dict:
        

        width, height = 400, 400
        unsplash_api_url = os.getenv('UNSPLASH_API_BASED_URL')
        if not unsplash_api_url:
            logging.error("L'URL d'API Unsplash n'est pas définie.")
            # logging.info(unsplash_api_url)
            # logging.info(data)
            return {}
        
        response = requests.get(dc.UNSPLASH_API_BASED_URL, params=SEARCH_PARAMS)
        data = response.json()
        logging.debug(data)
        # logging.debug(data['urls'])
    # Attribution aléatoire d'une image différente à chaque ville.
        city_photos = {}
        for city in cities:
            # Assurez-vous que vous avez assez de photos dans la réponse, sinon ajustez cela en conséquence.
            random_photo = random.choice(data)
            photo_url = f"{random_photo['urls']['raw']}?w={width}&h={height}&fit=crop"
            city_photos[city] = photo_url
        logging.error(f"L'URL d'API Unsplash est pas définie:{unsplash_api_url}")
        return city_photos
        
    def get_cities_with_photos(self):
        city_names = [house.city for house in self.house_repository.get_all()]
        city_photos = self.get_photos(city_names)
        # print(city_photos)

        cities_with_photos = [{'name': city_name, 'photoUri': photoUri} for city_name, photoUri in city_photos.items()]

        return cities_with_photos

