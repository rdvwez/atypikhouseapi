from datetime import datetime
from app.users.models import UserModel
from app.users.repository import UserRepository
from tests.base_test import BaseTest


user_repository = UserRepository()

class UserTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():
            user = UserModel(
                name = "MOTO",
                firstname = "Julien" ,
                username = "juju",
                phone_number = "+33 06 45 96 32 45",
                email = "julien.moto@gmail.com",
                password = "12345",
                is_custom = True,
                is_owner = False,
                is_admin = False,
                birth_date = datetime.now(),
                gender = True,
                is_activated = True
            )

            user_repository.save(user)
            user_repository.commit()

            self.assertIsNotNone(user_repository.get_user_by_id(1), "Did not find a user with id1' after saving to db")

            user_repository.delete(user)
            user_repository.commit()
            self.assertEqual(len(user_repository.get_all()), 0)
