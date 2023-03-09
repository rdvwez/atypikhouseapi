import pytest

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'


def  test_get_all_thematics(client, init_database):
    response = client.get("/api/thematic")
    assert response.status_code == 200
    expected_thematics = [{'houses': [], 'id': 1, 'libelle': 'romantique', 'show': True}, {'houses': [], 'id': 2, 'libelle': 'familial', 'show': False}]
    assert len(response.json) == 2
    assert response.json == expected_thematics

def test_get_thematic(client, access_admin_token):
    response = client.get("/api/thematic/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'houses': [], 'id': 1, 'libelle': 'romantique',  'show': True}

def test_get_thematic_unauthorized(client, access_owner_token):
    response = client.get("/api/thematic/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403
    assert response.json == {}

def test_delete_thematic(client, access_admin_token):
    response = client.delete("/api/thematic/2", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_thematic_unauthorized(client, access_customer_token):
    response = client.delete("/api/thematic/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403

def test_update_thematic(client, access_admin_token):
    thematic_data = {"libelle": "thematic de test", "show": True}
    response = client.put("/api/category/1", json=thematic_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["libelle"] == "thematic de test"

def test_update_thematic_unauthorized(client, access_owner_token):
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/thematic/1", json=category_data, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_update_thematic_fresh_token_required(client, access_admin_expired_token):
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/thematic/1", json=category_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_thematic(client, access_admin_token):
    new_thematic = {
        "libelle": "Test thematic",
        "show": True
    }
    response = client.post("/api/thematic", json=new_thematic, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 201
    assert response.json.get("libelle") == new_thematic["libelle"]
    assert response.json.get("show") == new_thematic["show"]


def test_create_thematic_without_fresh_token(client, access_admin_expired_token):
    new_thematic = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/thematic", json=new_thematic, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_thematic_with_bad_acess(client, access_owner_token):
    new_thematic = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/thematic", json=new_thematic, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_get_houses_in_thematic(client, access_admin_token):
    response = client.get("/api/thematic/1/house", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
#     #TODO : add an assert when house will be added


