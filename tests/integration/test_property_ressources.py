import pytest

from .test_order import pytestmark

pytestmark = pytest.mark.run(order=4)

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'

def  test_get_all_property(client, init_database):
    response = client.get("/api/property")
    assert response.status_code == 200
    expected_categories = [{'category': {'id': 1, 'libelle': 'bulle'}, 'description': 'Good wifi added', 'id': 1, 'is_required': True, 'libelle': 'wifi', 'property_values': [{'id': 1, 'libelle': 'sfr'}]}, {'category': {'id': 2, 'libelle': 'cabane'}, 'description': 'Added', 'id': 2, 'is_required': True, 'libelle': 'Air conditioner', 'property_values': [{'id': 2, 'libelle': '2'}]}, {'category': {'id': 2, 'libelle': 'cabane'}, 'description': 'deletion', 'id': 3, 'is_required': True, 'libelle': 'Ta be deleted', 'property_values': []}]

    assert len(response.json) == 3
    assert response.json == expected_categories

def test_get_property(client, access_admin_token):
    response = client.get("/api/property/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'category': {'id': 1, 'libelle': 'bulle'}, 'description': 'Good wifi added', 'id': 1, 'is_required': True, 'libelle': 'wifi', 'property_values': [{'id': 1, 'libelle': 'sfr'}]}

def test_get_property_unauthorized(client, access_customer_token):
    # En tant que client non propriétaire, on ne peut pas récupérer une catégorie
    response = client.get("/api/property/2", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json == {}

def test_create_property(client, access_admin_token):
    new_property = {
        "libelle": "Test Property",
        "description" :"Test Property description",
    "is_required":True,
    "category_id":1
    }
    response = client.post("/api/property", json=new_property, headers={"Authorization": f"Bearer {access_admin_token}"})
  
    assert response.status_code == 201
    assert response.json.get("libelle") == new_property["libelle"]
    assert response.json.get("description") == new_property["description"]
    assert response.json.get("is_required") == new_property["is_required"]
    assert response.json.get("category")["id"] == new_property["category_id"]

def test_create_property_without_fresh_token(client, access_admin_expired_token):
    new_property = {
        "libelle": "Test Property",
        "description" :"Test Property description",
    "is_required":True,
    "category_id":1
    }
    response = client.post("/api/property", json=new_property, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_property_with_bad_acess(client, access_owner_token):
    new_property = {
        "libelle": "Test Property",
        "description" :"Test Property description",
        "is_required":True,
        "category_id":1
    }
    response = client.post("/api/property", json=new_property, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_update_property(client, access_admin_token):
    new_property = {
        "libelle": "wifi",
        "description" :"Good wifi",
        "is_required":True,
    }
    response = client.put("/api/property/1", json=new_property, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["description"] == "Good wifi"

def test_update_property_unauthorized(client, access_owner_token):
    # En tant que propriétaire connecté, on ne peut pas mettre à jour une catégorie
    new_property = {
        "libelle": "wifi",
        "description" :"Good wifi",
        "is_required":True,
    }
    response = client.put("/api/property/1", json=new_property, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_update_property_fresh_token_required(client, access_admin_expired_token):
    new_property = {
        "libelle": "wifi",
        "description" :"Good wifi",
        "is_required":True,
    }
    response = client.put("/api/property/1", json=new_property, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401
