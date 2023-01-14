from datetime import datetime
from enum import unique

from app.db import db
from app.users.models import UserModel
from app.thematics.models import ThematicModel
from app.values.models import ValueModel
from app.images.models import ImageModel

class HouseModel(db.Model):

    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    # part_number = db.Column(db.Integer  , nullable=False)
    bedroom_number = db.Column(db.Integer, nullable=False)
    person_number = db.Column(db.Integer, nullable=False)
    parking_distance = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(60), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    area = db.Column(db.Integer, nullable=False)
    water = db.Column(db.Boolean, default=False)
    power = db.Column(db.Boolean, default=False)
    price = db.Column(db.Integer,nullable=False)
    latitude = db.Column(db.Float(30),nullable=False)
    longitude = db.Column(db.Float(30),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)
    thematic_id = db.Column(db.Integer, db.ForeignKey("thematics.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship("UserModel", back_populates = "houses")
    category = db.relationship("CategoryModel", back_populates = "houses")
    thematic = db.relationship("ThematicModel", back_populates = "houses")
    images = db.relationship("ImageModel", back_populates="house", lazy = "dynamic")
    

    def __repr__(self) -> dict:
        return self.__dict__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)