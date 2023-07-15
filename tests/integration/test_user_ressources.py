import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest import mock

from .test_order import pytestmark

pytestmark = pytest.mark.run(order=3)



@pytest.fixture
def access_admin_expired_token(client, freeze_datetime):
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'

# @pytest.mark.freeze_time("2023-06-03 10:00:00", tick=0)
def test_get_all_user(client,init_database, access_admin_token):

    expected_users = [{'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'jhon.doe@gmail.com', 'firstname': 'Jhon', 'gender': True, 'houses': [], 'id': 1, 'images': [], 'is_activated': True, 'is_admin': True, 'is_customer': True, 'is_owner': True, 'name': 'Doe', 'phone_number': '0669567821', 'updated_at': None, 'username': '@JDoe', 'values': []}, {'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'jannete.dhoe@gmail.com', 'firstname': 'Jannete', 'gender': False, 'houses': [{'address': '02 here and there', 'area': 8, 'bedroom_number': 2, 'city': 'Brest', 'country': 'France', 'description': 'Good first house', 'id': 1, 'latitude': 25.69, 'libelle': 'first house', 'longitude': 14.35, 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}, {'address': '06 here and there', 'area': 12, 'bedroom_number': 3, 'city': 'Lyon', 'country': 'France', 'description': 'Good second house', 'id': 2, 'latitude': 15.69, 'libelle': 'second house', 'longitude': 11.35, 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'water': False}, {'address': '06 here and there', 'area': 12, 'bedroom_number': 3, 'city': 'Lyon', 'country': 'France', 'description': 'Good second house', 'id': 3, 'latitude': 15.69, 'libelle': 'third house', 'longitude': 11.35, 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'water': False}], 'id': 2, 'images': [{'basename': 'front.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 1, 'is_avatar': False, 'path': '/media/house/', 'size': 34, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}, {'basename': 'back.jp', 'extension': '.jpg', 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, 'id': 2, 'is_avatar': False, 'path': '/media/house/', 'size': 43, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}, {'basename': 'deletion_test_image.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 3, 'is_avatar': False, 'path': 'fixtures/medias/deletion_test_image.jpg', 'size': 54881, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}], 'is_activated': True, 'is_admin': False, 'is_customer': True, 'is_owner': True, 'name': 'Dhoe', 'phone_number': '0669568821', 'updated_at': None, 'username': '@JDhoe', 'values': [{'id': 1, 'libelle': 'sfr'}, {'id': 2, 'libelle': '2'}]}, {'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'joseph.henry@gmail.com', 'firstname': 'Joseph', 'gender': True, 'houses': [], 'id': 3, 'images': [], 'is_activated': True, 'is_admin': False, 'is_customer': True, 'is_owner': False, 'name': 'Henry', 'phone_number': '0669569821', 'updated_at': None, 'username': '@JHenry', 'values': []}, {'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'charles.bot@gmail.com', 'firstname': 'Charles', 'gender': True, 'houses': [], 'id': 4, 'images': [], 'is_activated': True, 'is_admin': False, 'is_customer': True, 'is_owner': False, 'name': 'Bot', 'phone_number': '0669567821', 'updated_at': None, 'username': '@CBot', 'values': []}, {'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'yatch.nomi@gmail.com', 'firstname': 'Yatch', 'gender': True, 'houses': [], 'id': 5, 'images': [], 'is_activated': False, 'is_admin': False, 'is_customer': True, 'is_owner': False, 'name': 'Nomi', 'phone_number': '0664567821', 'updated_at': None, 'username': '@YNomi', 'values': []}]

    response = client.get("/api/user",headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert expected_users == response.json

def test_get_all_user_with_bad_rigth(client,init_database, access_owner_token):

    response = client.get("/api/user",headers={"Authorization": f"Bearer {access_owner_token}"})
    
    assert response.status_code == 403

def test_register(client,init_database):
    credentiels = { "email":"julien.moto@gmail.com","password":"12345",}

    with  mock.patch("app.users.service.send_confirmation_account_mail") as mock_send_confirmation_account_mail:
        mock_send_confirmation_account_mail.return_value = None


        response = client.post("/api/register", json=credentiels)
        assert response.status_code == 201
        assert response.json["message"] == "Account created successfully, an email with the activation link has been sent to your emeil addresse, please check."

def test_active_user_account(client,init_database):
    
    response = client.get("/api/user_confirm/5")
    assert response.status_code == 200

def test_confirm_fake_user(client,init_database):
    
    response = client.get("/api/user_confirm/23456")
    assert response.status_code == 404
    assert response.json["status"]  == "Not Found"

def test_delete_user(client,init_database, access_admin_token):

    response = client.delete("/api/user/5",headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 200

def test_delete_fake_user(client,init_database, access_admin_token):

    response = client.delete("/api/user/7",headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 404

def test_delete_user_with_bad_rigth(client,init_database, access_customer_token):

    response = client.delete("/api/user/3",headers={"Authorization": f"Bearer {access_customer_token}"})

    assert response.status_code == 403

def test_logout(client,init_database, access_customer_token):
    response = client.get("/api/logout",headers={"Authorization": f"Bearer {access_customer_token}"})
    # breakpoint()
    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out."

def test_logout_when_not_login(client,init_database, access_admin_expired_token):
    response = client.get("/api/logout",headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401
    assert response.json["message"] ==  "Signature verification failled."
    assert response.json["error"] == "invalid token"

def test_confirm_activated_user_account(client,init_database):
    
    response = client.get("/api/user_confirm/3")
    assert response.status_code == 400
    assert response.json["message"]  == "Account already confirmed"

def test_set_user_pasword(client,init_database,access_customer_token):
    
    new_password = {"password": "123456",}

    response = client.post("/api/user/password", json=new_password, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 201
   


def test_login(client,init_database):
    credentiels = {
        "email":"jannete.dhoe@gmail.com",
        "password":"password2",
        }
    response = client.post("/api/login", json=credentiels)
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json

def test_login_with_bad_credentials(client,init_database):
    credentiels = {
        "email":"jannete.dhoe@gmail.com",
        "password":"passwor",
        }
    response = client.post("/api/login", json=credentiels)
    assert response.status_code == 401
    assert response.json["status"] == "Unauthorized"



def test_refresh_token_with_not_fresh_token(client,init_database, access_admin_expired_token):
    response = client.get("/api/refresh",headers={"Authorization": f"Bearer {access_admin_expired_token}"})

    assert response.status_code == 401
    assert response.json["message"] ==  "Signature verification failled."
    assert response.json["error"] == "invalid token"

def test_refresh_token(client,init_database, access_owner_token):
    

    with  mock.patch("app.users.service.create_access_token") as mock_create_access_token:
        
        mock_create_access_token.return_value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY26JWM"
        response = client.get("/api/refresh",headers={"Authorization": f"Bearer {access_owner_token}"})

        assert response.status_code == 200
        assert response.json["access_token"] ==  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY26JWM'


def test_get_user_by_id(client,init_database, access_admin_token):

    expected_user = {'birth_date': '2023-06-03', 'created_at': '2023-06-03T10:00:00', 'email': 'charles.bot@gmail.com', 'firstname': 'Charles', 'gender': True, 'houses': [], 'id': 4, 'images': [], 'is_activated': True, 'is_admin': False, 'is_customer': True, 'is_owner': False, 'name': 'Bot', 'phone_number': '0669567821', 'updated_at': None, 'username': '@CBot', 'values': []}

    response = client.get("/api/user/4",headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 200
    assert response.json   == expected_user


def test_get_user_by_id_with_bad_rigth(client,init_database, access_owner_token):

    response = client.get("/api/user/4",headers={"Authorization": f"Bearer {access_owner_token}"})

    assert response.status_code == 403








    
    