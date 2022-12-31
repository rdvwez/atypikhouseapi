from datetime import datetime
from app.db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    firstname = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    is_custom = db.Column(db.Boolean, nullable=False, default=False)
    is_owner = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_activated = db.Column(db.Boolean, default=False)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    houses = db.relationship("HouseModel", back_populates="user", lazy = "dynamic")
    values = db.relationship("ValueModel", back_populates="user", lazy = "dynamic")
    images = db.relationship("ImageModel", back_populates="user", lazy = "dynamic")

    def __repr__(self) -> dict:
        return self.__dict__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)