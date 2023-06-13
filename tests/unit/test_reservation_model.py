from unittest import TestCase
from app.reservations.models import ReservationModel
from app.houses.models import HouseModel
from app.users.models import UserModel


class ReservationTest(TestCase):

    def test_create_reservation(self):
        reservation = ReservationModel(
            status="pending",
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",

            )
        self.assertEqual('pending',reservation.status)
        self.assertEqual(52.75,reservation.amount)
        self.assertEqual('13/08/2023',reservation.start_date)
        self.assertEqual('10/09/2023',reservation.end_date)

    def test_repr(self):
        reservation = ReservationModel(
            status="pending",
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",
            )
        reservation_dict_representation = reservation.__repr__()
        del reservation_dict_representation["_sa_instance_state"]
        self.assertEqual(reservation_dict_representation, {
            "status":"pending",
            "amount":52.75,
            "start_date":"13/08/2023",
            "end_date":"10/09/2023",})
    
    def test_create_reservation_without_status(self):
        reservation = ReservationModel(
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",
            )

        self.assertIsNone(reservation.status)

    def test_create_reservation_without_amount(self):
        reservation = ReservationModel(
            status="pending",
            start_date="13/08/2023",
            end_date="10/09/2023",
            )

        self.assertIsNone(reservation.amount)


    def test_user_reservation(self):

        user = UserModel(
            id=1,
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_customer = True,
            is_owner = False,
            is_admin = False,
        )

        reservation = ReservationModel(
            status="pending",
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",
            user_id = 1,
            user = user
            )

        self.assertEqual(reservation.__repr__().get("user_id"), user.id)

    def test_house_reservtion(self):

        house = HouseModel(
            id = 1,
            libelle = "libelle",
            description = "description de la house",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            address = "44 rue des vaujours",
            city = "paris",
            country = "france",
            area = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
        )

        reservation = ReservationModel(
            status="pending",
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",
            house_id = 1,
            house = house
            )

        self.assertEqual(reservation.__repr__().get("house_id"), house.id)
    
    def test_create_reservation_without_wrong_column_type(self):
        reservation = ReservationModel(
            status="pending",
            amount=52.75,
            start_date="13/08/2023",
            end_date="10/09/2023",
            )
        self.assertNotEqual(type(reservation.status), "<class 'str'>")
        self.assertNotEqual(type(reservation.start_date), "<class 'str'>")
        self.assertNotEqual(type(reservation.end_date), "<class 'str'>")