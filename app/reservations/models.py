import enum
from datetime import datetime
from enum import unique
from sqlalchemy import Enum
# from sqlalchemy.dialects.postgresql import ENUM

from app.db import db

# status_enum = ENUM(*['pending', 'canceled','complete','failed', 'deleted'], name='status_enum')

# houses_to_reservation = db.Table(
#     "houses_to_reservation",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
#     db.Column("reservation_id", db.Integer, db.ForeignKey("reservations.id"))

# )
class ReservationStatus(enum.Enum):
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    DELETED = 'DELETED'

class ReservationModel(db.Model):

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    card_number = db.Column(db.String(16), nullable=False)
    card_exp_month = db.Column(db.Integer, nullable=False)
    card_exp_year = db.Column(db.Integer, nullable=False)
    cvc = db.Column(db.String(3), nullable=False)

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship("UserModel", )

    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable = True)
    house = db.relationship("HouseModel", )

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
   
    

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)