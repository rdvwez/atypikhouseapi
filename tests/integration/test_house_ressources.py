import pytest

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'


def  test_get_all_houses(client, init_database):
    response = client.get("/api/house")
    assert response.status_code == 200
    expected_houses = [{'address': '02 here and there', 'area': 8, 'bedroom_number': 2, 'category': {'id': 1, 'libelle': 'bulle'}, 'city': 'Brest', 'country': 'France', 'description': 'Good first house', 'id': 1, 'images': [{'basename': 'front', 'extension': '.jpg', 'is_avatar': False, 'path': '/media/house/', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}], 'latitude': 25.69, 'libelle': 'first house', 'longitude': 14.35, 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'thematic': {'id': 1, 'libelle': 'romantique'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, {'address': '06 here and there', 'area': 12, 'bedroom_number': 3, 'category': {'id': 2, 'libelle': 'cabane'}, 'city': 'Lyon', 'country': 'France', 'description': 'Good second house', 'id': 2, 'images': [{'basename': 'back', 'extension': '.jpg', 'is_avatar': False, 'path': '/media/house/', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}], 'latitude': 15.69, 'libelle': 'second house', 'longitude': 11.35, 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'thematic': {'id': 2, 'libelle': 'familial'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, {'address': '06 here and there', 'area': 12, 'bedroom_number': 3, 'category': {'id': 2, 'libelle': 'cabane'}, 'city': 'Lyon', 'country': 'France', 'description': 'Good second house', 'id': 3, 'images': [], 'latitude': 15.69, 'libelle': 'third house', 'longitude': 11.35, 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'thematic': {'id': 2, 'libelle': 'familial'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}]

    assert len(response.json) == 3
    assert response.json == expected_houses

def test_get_house(client,init_database, access_owner_token):
    response = client.get("/api/house/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'address': '02 here and there', 'area': 8, 'bedroom_number': 2, 'category': {'id': 1, 'libelle': 'bulle'}, 'city': 'Brest', 'country': 'France', 'description': 'Good first house', 'id': 1, 'images': [{'basename': 'front', 'extension': '.jpg', 'is_avatar': False, 'path': '/media/house/', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}], 'latitude': 25.69, 'libelle': 'first house', 'longitude': 14.35, 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'thematic': {'id': 1, 'libelle': 'romantique'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}


def test_get_house_unauthorized(client,init_database, access_customer_token):
    response = client.get("/api/house/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_update_house(client, init_database, access_admin_token):
    house_data = {
       "libelle" : "first house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France"
                  
    }
    
    response = client.put("/api/house/1", json=house_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["address"] == "03 here and there"

def test_update_house_unauthorized(client, init_database, access_customer_token):
    house_data = {
       "libelle" : "first house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France"          
    }
    response = client.put("/api/house/1", json=house_data, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_update_house_fresh_token_required(client, init_database, access_admin_expired_token):
    house_data = {
       "libelle" : "first house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France"          
    }
    response = client.put("/api/house/1", json=house_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_delete_house(client,init_database, access_admin_token):
    response = client.delete("/api/house/3", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_house_unauthorized(client,init_database, access_customer_token):
    response = client.delete("/api/value/3", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403


def test_create_house(client, init_database, access_admin_token):
    new_house = {
       "libelle" : "forth house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France",
        "category_id" : 2,
        "user_id" : 2,
        "thematic_id" : 3     
    }
    response = client.post("/api/house", json=new_house, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 201
    assert response.json == {'address': '03 here and there', 'area': 8, 'bedroom_number': 2, 'category': {'id': 2, 'libelle': 'cabane'}, 'city': 'Brest', 'country': 'France', 'description': 'Good first house', 'id': 4, 'images': [], 'latitude': 25.69, 'libelle': 'forth house', 'longitude': 14.35, 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'thematic': {'id': 3, 'libelle': 'To be deleted'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}


def test_create_house_without_fresh_token(client, init_database, access_admin_expired_token):
    new_house = {
       "libelle" : "forth house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France",
        "category_id" : 2,
        "user_id" : 2,
        "thematic_id" : 4       
    }
    response = client.post("/api/house", json=new_house, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_house_with_bad_acess(client, init_database, access_customer_token):
    new_house = {
       "libelle" : "forth house",
        "description" : "Good first house" ,
        "bedroom_number" : 2,
        "person_number" : 2,
        "parking_distance" : 3,
        "area" : 8, 
        "water" : True,
        "power" : True,
        "price" : 50,
        "latitude" : 25.69,
        "longitude" : 14.35,
        "address" : "03 here and there",
        "city" : "Brest",
        "country" : "France",
        "category_id" : 2,
        "user_id" : 2,
        "thematic_id" : 4       
    }
    response = client.post("/api/house", json=new_house, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403



