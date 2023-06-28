import stripe
import pytest

from unittest import mock

from .test_order import pytestmark

pytestmark = pytest.mark.run(order=8)


# def mock_create_payment_method():
#     return "pm_1NIqMm2eZvKYlo2CNKzeNgrM"
 
# def mock_create_stripe_customer():
#     return "cus_9s6XFG2Qq6Fe7v"

# def mock_create_subscription():
#     return "sub_1NLwpW2eZvKYlo2CNpSQtzDP"

# def mock_attach_paymentmethod_to_customer():
#     return "pm_1NIqMm2eZvKYlo2CNKzeNgrM"

# def mock_send_reservation_confirmation_mail():
#     return None


@pytest.fixture
def access_admin_expired_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'

@pytest.fixture
def access_customer_expired_token():
    return 'eyJhbGciOiJIUzI1N45sInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc4MzIwNzYwLCJqdGkiOiJiZTYwODA4Yi1iN2I4LTRlNjUtODkw...zE2MCwiaXNfY3VzdG9tIjp0cnVlLCJpc19vd25lciI6ZmFsc2UsImlzX2FkbWluIjpmYWxzZX0.mGqqJrcbhrBvhIFcLEadXMs5jYM91mGwGpwaVY25JWM'

def  test_get_all_reservation(client, init_database,access_customer_token):
    response = client.get("/api/reservation", headers={"Authorization": f"Bearer {access_customer_token}"})
    # breakpoint()
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json == [{'amount': 100.0, 'card_exp_month': 12, 'card_exp_year': 26, 'card_number': '4243424342434243', 'cvc': '465', 'end_date': None, 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 1, 'start_date': None, 'status': 'CANCELED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}, {'amount': 1000.0, 'card_exp_month': 1, 'card_exp_year': 27, 'card_number': '4243424342434224', 'cvc': '465', 'end_date': None, 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, 'id': 2, 'start_date': None, 'status': 'COMPLETED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}]



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
    assert response.json == {'amount': 100.0, 'card_exp_month': 12, 'card_exp_year': 26, 'card_number': '4243424342434243', 'cvc': '465', 'end_date': None, 'house': {'area': 8, 'description': 'Good first house', 'id': 1, 'libelle': 'first house', 'parking_distance': 3, 'person_number': 2, 'power': True, 'price': 50, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': True}, 'id': 1, 'start_date': None, 'status': 'CANCELED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}


def test_update_reservation(client, init_database, access_admin_token):
    reservation_data = {
        "status": "PENDING",
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        }
    response = client.put("/api/reservation/2", json=reservation_data, headers={"Authorization": f"Bearer {access_admin_token}"})

    assert response.status_code == 200
    assert response.json["status"] == "PENDING"
    assert response.json == {'amount': 1000.0, 'card_exp_month': 1, 'card_exp_year': 27, 'card_number': '4243424342434224', 'cvc': '465', 'end_date': '2023-04-01T00:00:00', 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, 'id': 2, 'start_date': '2023-03-10T00:00:00', 'status': 'PENDING', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}



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

def test_create_reservation(client, init_database,  access_customer_token):
    
    expected_reservation = {'amount': 100.0, 'card_exp_month': 6, 'card_exp_year': 2026, 'card_number': '4242424242424242', 'cvc': '178', 'end_date': '2023-04-01T00:00:00', 'house': {'area': 12, 'description': 'Good second house', 'id': 2, 'libelle': 'second house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'user': {'firstname': 'Jannete', 'id': '2', 'name': 'Dhoe'}, 'water': False}, 'id': 3, 'start_date': '2023-03-10T00:00:00', 'status': 'COMPLETED', 'user': {'firstname': 'Joseph', 'id': '3', 'name': 'Henry'}}
    new_reservation = {
        "amount": 100,
        "house_id": 1,
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        "card_number" : "4242424242424242",
        "card_exp_month" : 6,
        "card_exp_year" : 2026,
        "cvc" : "178",
        "user_id":3,
        "house_id": 2
    }

    with mock.patch("app.reservations.service.create_payment_method") as mock_create_payment_method,\
        mock.patch("app.reservations.service.create_stripe_customer") as mock_create_stripe_customer,\
        mock.patch("app.reservations.service.create_subscription") as mock_create_subscription,\
        mock.patch("app.reservations.service.attach_paymentmethod_to_customer") as mock_attach_paymentmethod_to_customer,\
        mock.patch("app.reservations.service.send_reservation_confirmation_mail") as mock_send_reservation_confirmation_mail:
        
        mock_create_payment_method.return_value = "pm_1NIqMm2eZvKYlo2CNKzeNgrM"
        mock_create_stripe_customer.return_value = "cus_9s6XFG2Qq6Fe7v"
        mock_create_subscription.return_value = "sub_1NLwpW2eZvKYlo2CNpSQtzDP"
        mock_attach_paymentmethod_to_customer.return_value = "pm_1NIqMm2eZvKYlo2CNKzeNgrM"
        mock_send_reservation_confirmation_mail.return_value = None

        response = client.post("/api/reservation", json=new_reservation, headers={"Authorization": f"Bearer {access_customer_token}"})
       
        assert mock_create_payment_method.call_args == mock.call(card_number="4242424242424242", card_exp_month=6, card_exp_year=2026, cvc='178')
        assert mock_create_stripe_customer.call_args == mock.call("joseph.henry@gmail.com")
        assert mock_create_subscription.call_args == mock.call("cus_9s6XFG2Qq6Fe7v", "pm_1NIqMm2eZvKYlo2CNKzeNgrM")
        assert mock_attach_paymentmethod_to_customer.call_args == mock.call("pm_1NIqMm2eZvKYlo2CNKzeNgrM", "cus_9s6XFG2Qq6Fe7v")
        
        assert response.status_code == 201
        assert response.json == expected_reservation


def test_create_reservation_without_fresh_token(client, init_database, access_customer_expired_token):
    new_reservation = {
        "amount": 100,
        "house_id": 1,
        "start_date": "2023-03-10T00:00:00",
        "end_date":"2023-04-01T00:00:00",
        "card_number" : "4242424242424242",
        "card_exp_month" : 6,
        "card_exp_year" : 2026,
        "cvc" : "178",
        "user_id":3,
        "house_id": 2
    }

    with mock.patch("app.reservations.service.create_payment_method") as mock_create_payment_method,\
        mock.patch("app.reservations.service.create_stripe_customer") as mock_create_stripe_customer,\
        mock.patch("app.reservations.service.create_subscription") as mock_create_subscription,\
        mock.patch("app.reservations.service.attach_paymentmethod_to_customer") as mock_attach_paymentmethod_to_customer,\
        mock.patch("app.reservations.service.send_reservation_confirmation_mail") as mock_send_reservation_confirmation_mail:
        
        mock_create_payment_method.return_value = "pm_1NIqMm2eZvKYlo2CNKzeNgrM"
        mock_create_stripe_customer.return_value = "cus_9s6XFG2Qq6Fe7v"
        mock_create_subscription.return_value = "sub_1NLwpW2eZvKYlo2CNpSQtzDP"
        mock_attach_paymentmethod_to_customer.return_value = "pm_1NIqMm2eZvKYlo2CNKzeNgrM"
        mock_send_reservation_confirmation_mail.return_value = None
        
        response = client.post("/api/reservation", json=new_reservation, headers={"Authorization": f"Bearer {access_customer_expired_token}"})

        assert response.status_code == 401

def test_delete_reservation(client,init_database, access_owner_token):
    response = client.delete("/api/reservation/1", headers={"Authorization": f"Bearer {access_owner_token}"})
    assert response.status_code == 204

def test_delete_reservation_unauthorized(client,init_database, access_customer_token):
    response = client.delete("/api/reservation/1", headers={"Authorization": f"Bearer {access_customer_token}"})
    assert response.status_code == 403





