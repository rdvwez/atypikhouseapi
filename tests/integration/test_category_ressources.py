import pytest

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'



def  test_get_all_categories(client, init_database):
    response = client.get("/api/category")
    assert response.status_code == 200
    expected_categories = [{'houses': [], 'id': 1, 'libelle': 'bulle', 'properties': [], 'show': True}, {'houses': [], 'id': 2, 'libelle': 'cabane', 'properties': [], 'show': False}]
    assert len(response.json) == 2
    assert response.json == expected_categories

def test_get_category(client, access_admin_token):
    # En tant que client connecté, on peut récupérer une catégorie existante
    response = client.get("/api/category/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'houses': [], 'id': 1, 'libelle': 'bulle', 'properties': [], 'show': True}

def test_get_category_unauthorized(client, access_owner_token):
    # En tant que client non propriétaire, on ne peut pas récupérer une catégorie
    response = client.get("/api/category/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403
    assert response.json == {}

def test_delete_category(client, access_admin_token):
    # En tant qu'administrateur connecté, on peut supprimer une catégorie existante
    response = client.delete("/api/category/2", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_category_unauthorized(client, access_customer_token):
    # En tant que propriétaire connecté, on ne peut pas supprimer une catégorie
    response = client.delete("/api/category/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403

def test_update_category(client, access_admin_token):
    # En tant qu'administrateur connecté, on peut mettre à jour une catégorie existante
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    assert response.json["libelle"] == "maisonnette"

def test_update_category_unauthorized(client, access_owner_token):
    # En tant que propriétaire connecté, on ne peut pas mettre à jour une catégorie
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_update_category_fresh_token_required(client, access_admin_expired_token):
    # En tant qu'administrateur connecté, un token frais est requis pour mettre à jour une catégorie
    category_data = {"libelle": "maisonnette", "show": True}
    response = client.put("/api/category/1", json=category_data, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_category(client, access_admin_token):
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 201
    assert response.json.get("libelle") == new_category["libelle"]
    assert response.json.get("show") == new_category["show"]


def test_create_category_without_fresh_token(client, access_admin_expired_token):
    # Créer une nouvelle catégorie
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_admin_expired_token}"})
    assert response.status_code == 401

def test_create_category_with_bad_acess(client, access_owner_token):
    # Créer une nouvelle catégorie
    new_category = {
        "libelle": "Test Category",
        "show": True
    }
    response = client.post("/api/category", json=new_category, headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 403

def test_get_houses_in_category(client, access_admin_token):
    response = client.get("/api/category/1/house", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 200
    #TODO : add an assert when house will be added


