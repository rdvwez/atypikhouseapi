from typing import Dict, Union, List
from datetime import datetime
from enum import unique

from app.db import db

# CategoryJSON = Dict[str, Union[int, str, bool, List[HouseJSON], List[PropertyJSON]]]

class ImageModel(db.Model):

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250), nullable=False)
    extension = db.Column(db.String(100), nullable=False)
    basename = db.Column(db.String(100), nullable=False)
    is_avatar = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = True)
    user = db.relationship("UserModel", back_populates = "images")
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable = True)
    house = db.relationship("HouseModel", back_populates = "images")

    def __repr__(self) -> dict:
        return self.__dict__

    def __init__(self,**kwargs):
        super().__init__(**kwargs)