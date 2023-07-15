from datetime import datetime
from enum import unique

from app.db import db

class PropertyModel(db.Model):

    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_required = db.Column(db.Boolean, nullable=False, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)
    category = db.relationship("CategoryModel", back_populates = "properties")
    property_values = db.relationship("ValueModel", back_populates="property_object", lazy = "dynamic")

    def __repr__(self) -> str:
        return str(self.__dict__)
    #     return str({
    #         'id':self.id,
    #         "libelle" :self.libelle,
    # "description" : self.description,
    # "is_required" : self.is_required,
    # "category_id" : self.category_id
    #     })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)