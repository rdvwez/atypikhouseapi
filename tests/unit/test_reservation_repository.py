from datetime import datetime

from app.reservations.models import ReservationModel
from app.categories.models import CategoryModel
from app.thematics.models import ThematicModel
from app.users.models import UserModel
from app.houses.models import HouseModel
from app.houses.repository import HouseRepository
from app.categories.repository import CategoryRepository
from app.thematics.repository import ThematicRepository
from app.users.repository import UserRepository
from app.reservations.repository import ReservationRepository
from tests.base_test import BaseTest


reservation_repository = ReservationRepository()
category_repository = CategoryRepository()
house_repository = HouseRepository()
thematic_repository = ThematicRepository()
user_repository = UserRepository()

class ReservationTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():
            user = UserModel(
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_custom = True,
            is_owner = False,
            is_admin = False,
        )
             
            cat = CategoryModel(
                libelle = "cabane dans les arbres", 
                show = True, 
            )

            them = ThematicModel(
                libelle="romantiques", 
                show=False
            )

            category_repository.save(cat)
            category_repository.commit()
            thematic_repository.save(them)
            thematic_repository.commit()
            user_repository.save(user)
            user_repository.commit()

            

            house = HouseModel(
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
            category_id = 1,
            user_id = 1,
            thematic_id = 1
            )

            house_repository.save(house)
            house_repository.commit()

            reservation = ReservationModel(
                status='pending', 
                amount=50,
                start_date = datetime.now(),
                end_date = datetime.now(),
                user_id=1,
                house_id=1
                )

            reservation_repository.save(reservation)
            reservation_repository.commit()

            self.assertIsNotNone(reservation_repository.get_reservation_by_id(1), "Did not find a reservation with id 1 after saving to db")

            reservation_repository.delete(reservation)
            reservation_repository.commit()
            self.assertEqual(len(reservation_repository.get_all()), 0)
