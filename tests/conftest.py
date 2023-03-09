import pytest
from flask import Flask
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta

from app.db import db
from main import create_app

from app.users.repository import UserRepository, UserModel
from app.images.repository import ImageRepository, ImageModel
from app.values.repository import ValueRepository, ValueModel
from app.houses.repository import HouseRepository, HouseModel
from app.thematics.repository import ThematicRepository, ThematicModel
from app.properties.repository import PropertyRepository, PropertyModel
from app.categories.repository import CategoryModel, CategoryRepository
from app.reservations.repository import ReservationRepository, ReservationModel
from app.reservations.repository import ReservationRepository, ReservationModel

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://desir:desirPass@127.0.0.1:3306/atypikbasetestpython"
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def init_database(app):
    # Ajout de catégories à la base de données
    category_repository = CategoryRepository()
    cat1= CategoryModel(libelle = "bulle", show = True)
    cat2= CategoryModel(libelle = "cabane", show = False)
    category_repository.save(cat1)
    category_repository.save(cat2)
    category_repository.commit()

    # Add thematics to database
    thematic_repositery = ThematicRepository()
    thematic1 = ThematicModel(libelle = "romantique", show = True)
    thematic2 = ThematicModel(libelle = "familial", show = False)
    thematic_repositery.save(thematic1)
    thematic_repositery.save(thematic2)
    thematic_repositery.commit()

    # Add properties to database
    property_repository = PropertyRepository()
    property_object1 = PropertyModel(libelle = "wifi",is_required=True, description = "Good wifi added", category_id=1)
    property_object2 = PropertyModel(libelle = "Air conditioner",is_required=True, description = "Added", category_id=2)
    property_repository.save(property_object1)
    property_repository.save(property_object2)
    property_repository.commit()
    # Add users to database
    user_repository = UserRepository()
    user1 = UserModel(
        name = "Doe",
        firstname = "Jhon",
        username = "@JDoe",
        phone_number = "0669567821",
        email = "jhon.doe@gmail.com",
        password = pbkdf2_sha256.hash("password1"),
        is_custom = True,
        is_owner = True,
        is_admin = True,
        is_activated = True,
        birth_date = datetime.now(),
        gender = True
    )
    user2 = UserModel(
        name = "Dhoe",
        firstname = "Jannete",
        username = "@JDhoe",
        phone_number = "0669568821",
        email = "jannete.dhoe@gmail.com",
        password = pbkdf2_sha256.hash("password2"),
        is_custom = True,
        is_owner =True,
        is_admin = False,
        is_activated = True,
        birth_date = datetime.now(),
        gender = False
    )

    user3 = UserModel(
        name = "Henry",
        firstname = "Joseph",
        username = "@JHenry",
        phone_number = "0669569821",
        email = "joseph.henry@gmail.com",
        password = pbkdf2_sha256.hash("password3"),
        is_custom = True,
        is_owner = False,
        is_admin = False,
        is_activated = True,
        birth_date = datetime.now(),
        gender = True
    )
    user_repository.save(user1)
    user_repository.save(user2)
    user_repository.save(user3)
    user_repository.commit()

    
@pytest.fixture(scope="function")
def access_admin_token(client):
    data = {
        "email": "jhon.doe@gmail.com",
        "password": "password1"
    }
    response = client.post("/api/login", json=data)
    # assert response.status_code == 200
    admin_token = response.json["access_token"]
    yield admin_token

@pytest.fixture(scope="function")
def access_owner_token(client):
    data = {
        "email": "jannete.dhoe@gmail.com",
        "password": "password2"
    }
    response = client.post("/api/login", json=data)
    owner_token = response.json["access_token"]
    yield owner_token 

@pytest.fixture(scope="function")
def access_customer_token(client):
    data = {
        "username": "@JHenry",
        "password": "password3"
    }
    response = client.post("/api/login", json=data)
    customer_token = response.json["access_token"]
    yield customer_token

    
# @pytest.fixture(scope="session", autouse=True)
# def cleanup_database():
#     yield
#     with app.app_context():
#         db.session.remove()
#         db.drop_all()

    # yield db

    # Suppression des données de test de la base de données
    # user_repository.delete(user1)
    # user_repository.delete(user2)
    # user_repository.delete(user3)
    # user_repository.commit()

    # category_repository.delete(cat1)
    # category_repository.delete(cat2)
    # category_repository.commit()