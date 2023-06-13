import pytest
import io
import os
import shutil


from app.images.repository import ImageRepository, ImageModel

@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'


def  test_get_all_images(client, init_database):
    response = client.get("/api/image")
    assert response.status_code == 200
    
    expected_images = [{'basename': 'front.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}, 'id': 1, 'is_avatar': False, 'path': '/media/house/', 'size': 34, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}, {'basename': 'back.jp', 'extension': '.jpg', 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'water': False}, 'id': 2, 'is_avatar': False, 'path': '/media/house/', 'size': 43, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}, {'basename': 'deletion_test_image.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}, 'id': 3, 'is_avatar': False, 'path': 'fixtures/medias/deletion_test_image.jpg', 'size': 54881, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}]

    assert len(response.json) == 3
    assert response.json == expected_images

def test_get_image(client,init_database, access_owner_token):
    response = client.get("/api/image/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json == {'basename': 'front.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}, 'id': 1, 'is_avatar': False, 'path': '/media/house/', 'size': 34, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}


def test_get_image_unauthorized(client,init_database, access_customer_token):
    response = client.get("/api/image/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403
    assert response.json["status"] == 'Forbidden'

def test_delete_image_with_safe_filename(client,init_database, access_admin_token):

    response1 = client.get("/api/image/3", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response1.status_code == 200
    assert response1.json is not None

    response = client.delete("/api/image/3", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 204

def test_delete_image_with_unsafe_filename(client,init_database, access_admin_token):

    response1 = client.get("/api/image/2", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response1.status_code == 200

    response = client.delete("/api/image/2", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 400    
    assert response.json == {'massage': 'Illegal filename back.jp requested'}

def test_delete_image_with_Not_existing(client,init_database, access_admin_token):

    response = client.delete("/api/image/4", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 404   

def test_delete_image_with_bad_path(client,init_database, access_admin_token):
    """
    Dans ce test c'est le path qui n'est pas le bon, 
    ca casse dans la delete route au  niveau de 'os.remove(image.path) ' 
    """

    response = client.delete("/api/image/1", headers={"Authorization": f"Bearer {access_admin_token}"})
    assert response.status_code == 500 
    assert response.json == {'massage': 'Internal server error: Fail to delete image'}

def test_delete_image_unauthorized(client,init_database, access_customer_token):
    response = client.delete("/api/image/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403


def test_create_image(client, init_database, access_owner_token, ):

    expected_image = {'basename': 'home_desir_Documents_lab_python_Hatypik_house_Api_Python_fixtures_medias_test_image_1.jpg', 'extension': '.jpg', 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}, 'id': 4, 'is_avatar': False, 'path': 'madias/home_desir_Documents_lab_python_Hatypik_house_Api_Python_fixtures_medias_test_image_1.jpg', 'size': 0, 'type_mime': 'image/jpeg', 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}}

    file_path = os.path.abspath("fixtures/medias/test_image_1.jpg")
    with open(file_path, 'rb') as file:

        response1 = client.post("/api/uploadimage", data={"image": file,  }, headers={"Authorization": f"Bearer {access_owner_token}"}, content_type='multipart/form-data')
    
    assert response1.status_code == 201

    image = {"house_id": 1}
    response2 = client.put(f"/api/image/{response1.json['id']}",json=image, headers={"Authorization": f"Bearer {access_owner_token}"})

    assert response2.status_code == 200
    assert expected_image == response2.json
    assert response2.json["house"] == {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'water': True}

    generated_file_path = os.path.abspath(f"static/images/madias/{response1.json['basename']}")
    os.remove(generated_file_path)

def test_create_image_without_fresh_token(client, init_database, access_admin_expired_token, ):

    file_path = os.path.abspath("fixtures/medias/test_image_1.jpg")
    with open(file_path, 'rb') as file:

        response1 = client.post("/api/uploadimage", data={"image": file,  }, headers={"Authorization": f"Bearer {access_admin_expired_token}"}, content_type='multipart/form-data')
    
    assert response1.status_code == 401



def test_create_image(client, init_database, access_customer_token, ):

    file_path = os.path.abspath("fixtures/medias/test_image_1.jpg")
    with open(file_path, 'rb') as file:

        response1 = client.post("/api/uploadimage", data={"image": file,  }, headers={"Authorization": f"Bearer {access_customer_token}"}, content_type='multipart/form-data')
    
    assert response1.status_code == 403

    
   

 
