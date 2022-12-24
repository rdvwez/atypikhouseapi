from typing import List

from app.db import db

from app.houses.models import HouseModel

class HouseRepository:

    """Persistence of houses"""

    def get_all(self) -> List[HouseModel]:
        return HouseModel.query.order_by(HouseModel.id).all()

    def get_house_by_id(self, house_id: int) -> HouseModel:
        house = HouseModel.query.get_or_404(house_id)
        return house
    
    def save(self, house: HouseModel) -> None:
        db.session.add(house)

    def delete(self, house: HouseModel) -> None:
        db.session.delete(house)

    def flush(self) -> None:
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rolback()