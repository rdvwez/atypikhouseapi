from typing import Dict
from app.db import db
from sqlalchemy import or_

from app.users.models import UserModel

class UserRepository:
    """Persistence of users"""

    def get_all(self):
        return UserModel.query.order_by(UserModel.id).all()

    def get_user_by_id(self, user_id: int) -> UserModel:
        return UserModel.query.get_or_404(user_id)

    def get_user_by_email_or_username(self, user_data:Dict[str, str])-> UserModel:
        
        return UserModel.query.filter(
            or_(
                UserModel.email == user_data.get("email", None),
                UserModel.username == user_data.get("username"),
            )).first()

    def get_user_by_email(self, email: str)-> UserModel:
         return UserModel.query.get_or_404(email)

    def save(self, user:UserModel)->None:
        db.session.add(user)
        self.commit()

    def delete(self, user:UserModel)->None:
        db.session.delete(user)

    def flush(self)->None:
        db.session.flush()

    def commit(self)->None:
        db.session.commit()

    def rollback(self)->None:
        db.session.rolback()