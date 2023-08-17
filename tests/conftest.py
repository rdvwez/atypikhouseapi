import io
import os
import pytest
import shutil
from PIL import Image
from flask import Flask
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from freezegun import freeze_time


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

# @pytest.fixture(scope="function")
# def create_test_image():
#     file_path = os.path.abspath("fixtures/medias/test_image_1.jpg")
#     copy_path = os.path.abspath("fixtures/medias/insertion_test_image.jpg")
#     shutil.copy(file_path, copy_path)
#     with open(copy_path, "rb") as f:
#         return Image.open(f)
    #     image_content = f
    # yield Image.open(io.BytesIO(image_content))


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://desir:desirPass@127.0.0.1:3306/atypikbasetestpython"
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    with app.app_context():
        db.drop_all()

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
@freeze_time("2023-06-03 10:00:00", tick=0) 
def freeze_datetime():
    pass
    # frozen_datetime = datetime(2023, 6, 3, 10, 0, 0)  # Set the desired frozen date and time

    # class FrozenDateTime:
    #     @classmethod
    #     def now(cls, tz=None):
    #         return frozen_datetime.replace(tzinfo=tz)

    #     @classmethod
    #     def utcnow(cls):
    #         return frozen_datetime

    # yield monkeypatch.setattr("datetime.datetime", FrozenDateTime)


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
# @freeze_time("2023-06-03 10:00:00", tick=0) 
def init_database(app):
    db.drop_all()
    db.create_all()
    # Ajout de catégories à la base de données
    category_repository = CategoryRepository()
    cat1= CategoryModel(libelle = "bulle", show = True)
    cat2= CategoryModel(libelle = "cabane", show = False)
    cat3= CategoryModel(libelle = "To be deleted", show = False)
    category_repository.save(cat1)
    category_repository.save(cat2)
    category_repository.save(cat3)
    category_repository.commit()

    # Add thematics to database
    thematic_repository = ThematicRepository()
    thematic1 = ThematicModel(libelle = "romantique", show = True)
    thematic2 = ThematicModel(libelle = "familial", show = False)
    thematic3 = ThematicModel(libelle = "To be deleted", show = False)
    thematic_repository.save(thematic1)
    thematic_repository.save(thematic2)
    thematic_repository.save(thematic3)
    thematic_repository.commit()

    # Add properties to database
    property_repository = PropertyRepository()
    property_object1 = PropertyModel(libelle = "wifi",is_required=True, description = "Good wifi added", category_id=1)
    property_object2 = PropertyModel(libelle = "Air conditioner",is_required=True, description = "Added", category_id=2)
    property_object3 = PropertyModel(libelle = "Ta be deleted",is_required=True, description = "deletion", category_id=2)
    property_repository.save(property_object1)
    property_repository.save(property_object2)
    property_repository.save(property_object3)
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
        is_customer = True,
        is_owner = True,
        is_admin = True,
        is_activated = True,
        birth_date = datetime(2023, 6, 3, 10, 0, 0),
        created_at = datetime(2023, 6, 3, 10, 0, 0),
        gender = True
    )
    user2 = UserModel(
        name = "Dhoe",
        firstname = "Jannete",
        username = "@JDhoe",
        phone_number = "0669568821",
        email = "jannete.dhoe@gmail.com",
        password = pbkdf2_sha256.hash("password2"),
        is_customer = True,
        is_owner =True,
        is_admin = False,
        is_activated = True,
        birth_date = datetime(2023, 6, 3, 10, 0, 0),
        created_at = datetime(2023, 6, 3, 10, 0, 0),
        gender = False
    )

    user3 = UserModel(
        name = "Henry",
        firstname = "Joseph",
        username = "@JHenry",
        phone_number = "0669569821",
        email = "joseph.henry@gmail.com",
        password = pbkdf2_sha256.hash("password3"),
        is_customer = True,
        is_owner = False,
        is_admin = False,
        is_activated = True,
        birth_date = datetime(2023, 6, 3, 10, 0, 0),
        created_at = datetime(2023, 6, 3, 10, 0, 0),
        gender = True
    )
    user4 = UserModel(
        name = "Bot",
        firstname = "Charles",
        username = "@CBot",
        phone_number = "0669567821",
        email = "charles.bot@gmail.com",
        password = pbkdf2_sha256.hash("password4"),
        is_customer = True,
        is_owner = False,
        is_admin = False,
        is_activated = True,
        birth_date = datetime(2023, 6, 3, 10, 0, 0),
        created_at = datetime(2023, 6, 3, 10, 0, 0),
        gender = True
    )
    user5 = UserModel(
        name = "Nomi",
        firstname = "Yatch",
        username = "@YNomi",
        phone_number = "0664567821",
        email = "yatch.nomi@gmail.com",
        password = "",
        is_customer = True,
        is_owner = False,
        is_admin = False,
        is_activated = False,
        birth_date = datetime(2023, 6, 3, 10, 0, 0),
        created_at = datetime(2023, 6, 3, 10, 0, 0),
        gender = True
    )
    user_repository.save(user1)
    user_repository.save(user2)
    user_repository.save(user3)
    user_repository.save(user4)
    user_repository.save(user5)
    user_repository.commit()

    # Add properties to database
    value_repository = ValueRepository()
    value1 = ValueModel(libelle = "sfr", property_id = 1, user_id=2)
    value2 = ValueModel(libelle = "2", property_id = 2, user_id=2)
    value_repository.save(value1)
    value_repository.save(value2)
    value_repository.commit()

    # Add Houses to database
    house_repository = HouseRepository()
    house1 = HouseModel(
        libelle = "first house",
        description = "Good first house" ,
        category_id = 1,
        bedroom_number = 2,
        person_number = 2,
        parking_distance = 3,
        area = 8, 
        water = True,
        power = True,
        price = 50,
        latitude = 25.69,
        longitude = 14.35,
        thematic_id = 1,
        user_id = 2,
        address = "02 here and there",
        city = "Brest",
        country = "France"
    )
    house2 = HouseModel(
        libelle = "second house",
        description = "Good second house" ,
        category_id = 2,
        bedroom_number = 3,
        person_number = 3,
        parking_distance = 5,
        area = 12, 
        water = False,
        power = True,
        price = 60,
        latitude = 15.69,
        longitude = 11.35,
        thematic_id = 2,
        user_id = 2,
        address = "06 here and there",
        city = "Lyon",
        country = "France"
    )
    house3 = HouseModel(
        libelle = "third house",
        description = "Good second house" ,
        category_id = 2,
        bedroom_number = 3,
        person_number = 3,
        parking_distance = 5,
        area = 12, 
        water = False,
        power = True,
        price = 60,
        latitude = 15.69,
        longitude = 11.35,
        thematic_id = 2,
        user_id = 2,
        address = "06 here and there",
        city = "Lyon",
        country = "France"
    )

    house_repository.save(house1)
    house_repository.save(house2)
    house_repository.save(house3)
    house_repository.commit()

    # Add images to database
    image_repository = ImageRepository()

    image1 = ImageModel(
        path= "/media/house/", 
        basename="front.jpg",
        extension=".jpg", 
        user_id=2, 
        house_id= 1,
        type_mime = "image/jpeg",
        size = 34)
    image2 = ImageModel(
        path= "/media/house/", 
        basename="back.jp",
        extension=".jpg",
        type_mime = "image/jpeg",
        size= 43,
        user_id=2, 
        house_id= 2)

    file_path = os.path.abspath("fixtures/medias/test_image_1.jpg")
    copy_path = os.path.abspath("fixtures/medias/deletion_test_image.jpg")
    shutil.copy(file_path, copy_path)

    with open(copy_path, "rb") as f:
        image_content = f.read()
    image =  Image.open(io.BytesIO(image_content))

    image_data = io.BytesIO()
    image.save(image_data, format="JPEG")
    image_data = image_data.getvalue()

    image_object = ImageModel(
        path= "fixtures/medias/deletion_test_image.jpg", 
        basename="deletion_test_image.jpg",
        extension=".jpg", 
        type_mime = "image/jpeg",
        size= 54881,
        user_id=2, 
        house_id= 1)

    
    image_repository.save(image1)
    image_repository.save(image2)
    image_repository.save(image_object)
    image_repository.commit()

    # Add reservation to database
    reservation_repository = ReservationRepository()
    reservation1 = ReservationModel(
        status = "CANCELED",
        amount = 100,
        user_id = 3,
        house_id = 1,
        card_number  = "4243424342434243",
        card_exp_month  = 12,
        card_exp_year  = 26,
        cvc = 465,
        start_date = datetime(2023, 6, 3, 10, 0, 0),
        end_date = datetime(2023, 6, 9, 10, 0, 0)
    )
    reservation2 = ReservationModel(
        status = "COMPLETED",
        amount = 1000,
        user_id = 3,
        house_id = 2,
        card_number  = "4243424342434224",
        card_exp_month  = 1,
        card_exp_year  = 27,
        cvc = 465,
        start_date = datetime(2023, 6, 10, 10, 0, 0),
        end_date = datetime(2023, 6, 13, 10, 0, 0)
    )
    reservation_repository.save(reservation1)
    reservation_repository.save(reservation2)
    reservation_repository.commit()

    # yield 
    yield  # Permet d'exécuter les tests

    # Nettoyage après les tests
    db.session.rollback()
    db.drop_all()

    # reservation_repository.delete_all()
    # image_repository.delete_all()
    # value_repository.delete_all()
    # house_repository.delete_all()
    # thematic_repository.delete_all()
    # property_repository.delete_all()
    # category_repository.delete_all()
    # user_repository.delete_all()

    # reservation_repository.commit()
    # image_repository.commit()
    # value_repository.commit()
    # house_repository.commit()
    # thematic_repository.commit()
    # property_repository.commit()
    # category_repository.commit()
    # user_repository.commit()

    # db.session.remove()
    # db.drop_all()


    
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
# def cleanup_database(app):
#     yield
#     with app.app_context():
#         db.session.remove()
#         db.drop_all()

    # yield 

    # Suppression des données de test de la base de données
    # user_repository.delete(user1)
    # user_repository.delete(user2)
    # user_repository.delete(user3)
    # user_repository.commit()

    # category_repository.delete(cat1)
    # category_repository.delete(cat2)
    # category_repository.commit()