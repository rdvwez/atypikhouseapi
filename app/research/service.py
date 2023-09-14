from typing import List
from datetime import datetime
from flask import abort 
from typing import List, Dict, Tuple, Literal
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import  get_jwt_identity
from dataclasses import dataclass


from app.categories.repository import CategoryRepository
from app.thematics.repository import ThematicRepository
from app.houses.repository import HouseRepository
from app.houses.models import HouseModel
from app.reservations.repository import ReservationRepository
from app.reservations.models import ReservationModel

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
        self.category_repository = CategoryRepository()
        self.thematic_repository = ThematicRepository()
        self.house_repository = HouseRepository()
        self.reservation_repository = ReservationRepository()

    def sort_houses_by_category_id(self, houses:List[HouseModel], category_id:int)-> List[HouseModel]:
        return [house for house in houses if house.category_id == category_id]
    
    def sort_houses_by_thematic_id(self, houses:List[HouseModel], thematic_id:int)-> List[HouseModel]:
        return [house for house in houses if house.thematic_id == thematic_id]
    
    def sort_houses_by_nbr_person(self, houses:List[HouseModel], person_nbr:int)-> List[HouseModel]:
        return [house for house in houses if house.person_number == person_nbr]

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

    def find_available_houses(self, research_object:Research)->List[HouseModel]:
        houses = self.house_repository.get_all()

        cat_sorted_houses =  self.sort_houses_by_category_id(houses=houses, category_id =research_object.category_id)

        cat_them_sorted_houses =  self.sort_houses_by_thematic_id(houses=cat_sorted_houses, thematic_id=research_object.thematic_id)

        cat_them_np_sorted_houses = self.sort_houses_by_nbr_person(houses=cat_them_sorted_houses, person_nbr=research_object.person_nbr)

        completed_reservations = self.reservation_repository.get_reservations_by_status(status='completed')

        reserved_house_ids = [reservation.house_id for reservation in completed_reservations]

        non_available_house_ids = self.get_non_available_house_ids( 
                                            cat_them_np_sorted_houses, 
                                            reserved_house_ids,
                                            research_object,
                                            completed_reservations)
                
        available_houses = [sorted_house for sorted_house in  cat_them_np_sorted_houses if sorted_house.id not in non_available_house_ids]
        
        return available_houses
