from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.users.repository import UserRepository
from flask import abort

def owner_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_repository = UserRepository()
        curent_user = user_repository.get_user_by_id(get_jwt_identity())
        if not curent_user.is_owner :
            abort(403)
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_repository = UserRepository()
        curent_user = user_repository.get_user_by_id(get_jwt_identity())
        if not curent_user.is_admin :
            abort(403)
        return func(*args, **kwargs)
    return decorated_function

def customer_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_repository = UserRepository()
        curent_user = user_repository.get_user_by_id(get_jwt_identity())
        if not curent_user.is_customer :
            abort(403)
        return func(*args, **kwargs)
    return decorated_function