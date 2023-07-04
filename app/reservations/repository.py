from typing import List

from app.db import db
from app.reservations.models import ReservationModel


class ReservationRepository:

    """Persistence of Reservations"""

    def get_all(self) -> List[ReservationModel]:
        return ReservationModel.query.order_by(ReservationModel.id).all()
    
    def delete_all(self) -> None: # type: ignore
        ReservationModel.query.delete()

    def get_reservation_by_id(self, reservation_id: int) -> ReservationModel:
        reservation = ReservationModel.query.get_or_404(reservation_id)
        return reservation
    
    def delete_all(self) -> None:
        ReservationModel.query.delete()

    def save(self, reservation: ReservationModel) -> None:
        db.session.add(reservation)

    def delete(self, reservation: ReservationModel) -> None:
        db.session.delete(reservation)

    def flush(self) -> None:
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rolback()