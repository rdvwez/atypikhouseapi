from datetime import datetime
from enum import unique

from app.db import db

class ThematicModel(db.Model):

    __tablename__ = "thematics"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(40), unique=True, nullable=False)
    show = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    houses = db.relationship("HouseModel", back_populates="thematic", lazy = "dynamic")
    

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)