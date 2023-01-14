from datetime import datetime
from enum import unique
from app.properties.models import PropertyModel

from app.db import db

class ValueModel(db.Model):

    __tablename__ = "values"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(40), unique=True, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    property_object = db.relationship("PropertyModel", back_populates = "values")
    user = db.relationship("UserModel", back_populates = "values")

    def __repr__(self) -> dict:
        return self.__dict__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)