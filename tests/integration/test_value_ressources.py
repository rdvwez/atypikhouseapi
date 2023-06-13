import pytest

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'


def  test_get_all_values(client, init_database):
    response = client.get("/api/value")
    assert response.status_code == 200
    expected_values = [{'id': 1, 'libelle': 'sfr', 'property_object': {'id': 1, 'libelle': 'wifi'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}, {'id': 2, 'libelle': '2', 'property_object': {'id': 2, 'libelle': 'Air conditioner'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}]
    assert len(response.json) == 2
    assert response.json == expected_values

def test_get_value(client,init_database, access_owner_token):
    response = client.get("/api/value/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'id': 1, 'libelle': 'sfr', 'property_object': {'id': 1, 'libelle': 'wifi'}, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}

def test_get_value_unauthorized(client,init_database, access_customer_token):
    response = client.get("/api/value/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_delete_value(client,init_database, access_admin_token):
    response = client.delete("/api/value/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_value_unauthorized(client,init_database, access_customer_token):
    response = client.delete("/api/value/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403

def test_update_value(client, init_database, access_admin_token):
    value_data = {"libelle": "free"}
    response = client.put("/api/value/2", json=value_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["libelle"] == "free"

def test_update_value_unauthorized(client, init_database, access_customer_token):
    value_data = {"libelle": "bouygues"}
    response = client.put("/api/value/2", json=value_data, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_update_value_fresh_token_required(client, init_database, access_admin_expired_token):
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/value/2", json=category_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_value(client, init_database, access_admin_token):
    new_value = {
        "libelle": "lyca",
        "property_id" : 1, 
        "user_id":2
    }
    response = client.post("/api/value", json=new_value, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 201
    assert response.json.get("libelle") == new_value["libelle"]


def test_create_value_without_fresh_token(client, init_database, access_admin_expired_token):
    new_value = {
        "libelle": "lyca",
        "property_id" : 1, 
        "user_id":2
    }
    response = client.post("/api/value", json=new_value, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_value_with_bad_acess(client, init_database, access_customer_token):
    new_value = {
        "libelle": "lyca",
        "property_id" : 1, 
        "user_id":2
    }
    response = client.post("/api/value", json=new_value, headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403



