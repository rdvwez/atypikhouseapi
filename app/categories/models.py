from typing import Dict, Union, List
from datetime import datetime
from enum import unique
from app.houses.models import HouseModel

from app.db import db

# CategoryJSON = Dict[str, Union[int, str, bool, List[HouseJSON], List[PropertyJSON]]]

class CategoryModel(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(40), unique=True, nullable=False)
    show = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    houses = db.relationship("HouseModel", back_populates="category", lazy = "dynamic")
    properties = db.relationship("PropertyModel", back_populates="category", lazy = "dynamic")

    def __repr__(self) -> dict:
        return self.__dict__

    def __init__(self,**kwargs):
        super().__init__(**kwargs)