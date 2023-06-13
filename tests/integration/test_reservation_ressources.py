import pytest

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'

@pytest.fixture
def access_customer_expired_token():
    return 'eyJhbGciOiJIUzI1N45sInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'


def  test_get_all_reservation(client, init_database,access_customer_token):
    response = client.get("/api/reservation", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json == [{'end_date': '2023-03-13T00:00:00', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 1, 'start_date': '2023-03-01T00:00:00', 'status': 'CANCELED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}, {'end_date': '2023-03-10T00:00:00', 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, 'id': 2, 'start_date': '2023-04-01T00:00:00', 'status': 'COMPLETED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}]




def  test_get_all_reservation_with_expired_token(client, init_database,access_customer_expired_token):
    response = client.get("/api/reservation", headers={"Authorization": f"Bearer {access_customer_expired_token}"})
  
    assert response.status_code == 401

def  test_get_all_reservation_as_owber(client, init_database,access_owner_token):
    response = client.get("/api/reservation", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 200
    assert response.json == []


def test_get_reservation(client,init_database, access_customer_token):
    response = client.get("/api/reservation/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'end_date': '2023-03-13T00:00:00', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 1, 'start_date': '2023-03-01T00:00:00', 'status': 'CANCELED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}

def test_delete_reservation(client,init_database, access_owner_token):
    response = client.delete("/api/reservation/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 204

def test_delete_reservation_unauthorized(client,init_database, access_customer_token):
    response = client.delete("/api/reservation/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403

def test_update_reservation(client, init_database, access_admin_token):
    reservation_data = {
        "status": "PENDING",
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        }
    response = client.put("/api/reservation/2", json=reservation_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["status"] == "PENDING"



def test_update_reservation_unauthorized(client, init_database, access_customer_token):
    reservation_data = {
        "status": "PENDING",
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        }
    response = client.put("/api/reservation/2", json=reservation_data, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_update_reservation_fresh_token_required(client, init_database, access_admin_expired_token):
    reservation_data = {
        "status": "PENDING",
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        }
    response = client.put("/api/reservation/2", json=reservation_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

# def test_create_reservation(client, init_database, access_admin_token):
#     new_reservation = {
#         "amount": 100,
#         "house_id": 1,
#         "start_date": "2023-03-10T00:00:00",
#         "end_date":"2023-04-01T00:00:00",
#     }
#     response = client.post("/api/reservation", json=new_reservation, headers={"Authorization": f"Bearer {access_admin_token}"})
#     assert response.status_code == 201
#     assert response.json.get("amount") == new_reservation["amount"]
#     assert response.json.get("start_date") == new_reservation["start_date"]
#     assert response.json.get("end_date") == new_reservation["end_date"]


def test_create_reservation_without_fresh_token(client, init_database, access_customer_expired_token):
    new_reservation = {
         "amount": 100,
        "house_id": 1,
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
    }
    response = client.post("/api/reservation", json=new_reservation, headers={"Authorization": f"Bearer {access_customer_expired_token}"})
    assert response.status_code == 401





