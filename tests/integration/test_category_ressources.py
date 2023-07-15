import pytest
from .test_order import pytestmark

pytestmark = pytest.mark.run(order=1)

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'



def  test_get_all_categories(client, init_database):
    response = client.get("/api/category")
    assert response.status_code == 200
    expected_categories = [{'houses': [{'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}], 'id': 1, 'libelle': 'bulle', 'properties': [{'id': 1, 'libelle': 'wifi'}], 'show': True}, {'houses': [{'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, {'area': 12, 'description': 'Good second house', 'id': 3, 'libelle': 'third house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}], 'id': 2, 'libelle': 'cabane', 'properties': [{'id': 2, 'libelle': 'Air conditioner'}, {'id': 3, 'libelle': 'Ta be deleted'}], 'show': False}, {'houses': [], 'id': 3, 'libelle': 'To be deleted', 'properties': [], 'show': False}]
    assert len(response.json) == 3
    assert response.json == expected_categories

def test_get_category(client,init_database, access_admin_token):
    # En tant que client connecté, on peut récupérer une catégorie existante
    
    response = client.get("/api/category/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    
    assert response.json == {'houses': [{'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}], 'id': 1, 'libelle': 'bulle', 'properties': [{'id': 1, 'libelle': 'wifi'}], 'show': True}


def test_get_category_unauthorized(client, init_database, access_owner_token):
    # En tant que client non propriétaire, on ne peut pas récupérer une catégorie
    response = client.get("/api/category/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403
    assert response.json['status'] == 'Forbidden'

def test_delete_category(client,init_database, access_admin_token):
    # En tant qu'administrateur connecté, on peut supprimer une catégorie existante
    response = client.delete("/api/category/3", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_category_unauthorized(client,init_database, access_customer_token):
    # En tant que propriétaire connecté, on ne peut pas supprimer une catégorie
    response = client.delete("/api/category/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403

def test_update_category(client,init_database, access_admin_token):
    # En tant qu'administrateur connecté, on peut mettre à jour une catégorie existante
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["libelle"] == "maisonnette"

def test_update_category_unauthorized(client,init_database, access_owner_token):
    # En tant que propriétaire connecté, on ne peut pas mettre à jour une catégorie
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_update_category_fresh_token_required(client,init_database, access_admin_expired_token):
    # En tant qu'administrateur connecté, un token frais est requis pour mettre à jour une catégorie
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_category(client,init_database, access_admin_token):
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 201
    assert response.json.get("libelle") == new_category["libelle"]
    assert response.json.get("show") == new_category["show"]


def test_create_category_without_fresh_token(client,init_database, access_admin_expired_token):
    # Créer une nouvelle catégorie
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_category_with_bad_acess(client, init_database,access_owner_token):
    # Créer une nouvelle catégorie
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_get_houses_in_category(client,init_database, access_admin_token):
    response = client.get("/api/category/1/house", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
#     #TODO : add an assert when house will be added

# def  test_get_all_thematics(client, init_database):
#     response = client.get("/api/thematic")
#     assert response.status_code == 200
#     expected_thematics = [{'houses': [{'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}], 'id': 1, 'libelle': 'romantique', 'show': True}, {'houses': [{'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, {'area': 12, 'description': 'Good second house', 'id': 3, 'libelle': 'third house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}], 'id': 2, 'libelle': 'familial', 'show': False}, {'houses': [], 'id': 3, 'libelle': 'To be deleted', 'show': False}]

#     assert len(response.json) == 3
#     assert response.json == expected_thematics


