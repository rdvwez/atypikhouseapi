from typing import Dict, Union, List
from datetime import datetime
from enum import unique

from app.db import db

# CategoryJSON = Dict[str, Union[int, str, bool, List[HouseJSON], List[PropertyJSON]]]

class ImageModel(db.Model):

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250), nullable=True)
    extension = db.Column(db.String(100), nullable=True)
    basename = db.Column(db.String(100), nullable=True)
    is_avatar = db.Column(db.Boolean, default=False)
    type_mime = db.Column(db.String(50), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship("UserModel", back_populates = "images")
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable = True)
    house = db.relationship("HouseModel", back_populates = "images")

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)