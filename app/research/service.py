from typing import List
from datetime import datetime
import logging
from flask import abort 
from typing import List, Dict, Tuple, Literal
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity
from dataclasses import dataclass


from app.houses.repository import HouseRepository
from app.houses.models import HouseModel
from app.reservations.models import ReservationModel
from app.reservations.service import ReservationService

@dataclass
class Research:
    category_id: int
    thematic_id: int
    start_date: datetime
    end_date: datetime
    person_nbr: int

class ResearchService:
    # @inject
    def __init__(self):
        self.house_repository = HouseRepository()
        self.reservation_service = ReservationService()

    def get_reservation(self, reservations: List[ReservationModel], house_id: int)-> ReservationModel:
        res = [reservation for reservation in reservations if reservation.house_id == house_id]
        return res[0]
    
    def get_non_available_house_ids(
            self, 
            cat_them_np_sorted_houses:List[HouseModel], 
            reserved_house_ids:List[int],
            research_object:Research,
            completed_reservations:List[ReservationModel])->List[int]:
        
        matched_house_ids = []
        for house in cat_them_np_sorted_houses:
            if house.id in reserved_house_ids:
                reserved_house = self.get_reservation(reservations=completed_reservations,house_id=house.id)
                if research_object.start_date < reserved_house.end_date:
                    matched_house_ids.append(house.id)  
        return  matched_house_ids                

        # search_result = [sorted_house for sorted_house in cat_them_np_sorted_houses if house.id not in  matched_house_ids]
    def get_houses_by_category_id(self, houses:List[HouseModel], category_id:int)-> List[HouseModel]:
        return [house for house in houses if house.category_id == category_id]
    
    def get_houses_by_thematic_id(self, houses:List[HouseModel], thematic_id:int)-> List[HouseModel]:
        return [house for house in houses if house.thematic_id == thematic_id]
    
    def get_houses_by_nbr_person(self, houses:List[HouseModel], person_nbr:int)-> List[HouseModel]:
        return [house for house in houses if house.person_number >= person_nbr]

    def find_available_houses(self, research_data: Dict[str, str]) -> List[HouseModel] | tuple[dict[str, str], Literal[422]]:
        try:
            research_object = Research(**self.reservation_service.format_reservation_dict_dates_from_str_to_datetime(research_data))
        except ValueError as e:
            logging.info('Erreur de conversion de date')
            logging.error(e)
            return {"message": "Erreur de conversion de date"}, 422
        houses = self.house_repository.get_all()
        current_date = datetime.now()

        # Filtrer par catégorie
        cat_sorted_houses = self.get_houses_by_category_id(houses,research_object.category_id)

        # Filtrer par thématique
        cat_them_sorted_houses = self.get_houses_by_thematic_id(cat_sorted_houses, research_object.thematic_id)

        # Filtrer par nombre de personnes
        cat_them_np_sorted_houses = self.get_houses_by_nbr_person(cat_them_sorted_houses, research_object.person_nbr)

        # # Filtrer les maisons non disponibles
        # non_available_house_ids = set(
        #     house.id
        #     for house in cat_them_np_sorted_houses
        #     if research_object.start_date > house.end_date
        #     and current_date < research_object.start_date  # Vérification supplémentaire
        # )

        # # Filtrer les maisons disponibles
        # available_houses = [
        #     sorted_house
        #     for sorted_house in cat_them_np_sorted_houses
        #     if sorted_house.id not in non_available_house_ids
        # ]

        return cat_them_np_sorted_houses
