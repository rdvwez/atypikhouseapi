from datetime import datetime
from app.values.models import ValueModel
from app.users.models import UserModel
from app.categories.models import CategoryModel
from app.properties.models import PropertyModel
from app.values.repository import ValueRepository
from app.properties.repository import PropertyRepository
from app.users.repository import UserRepository
from app.categories.repository import CategoryRepository
from tests.base_test import BaseTest


value_repository = ValueRepository()
property_repository = PropertyRepository()
user_repository = UserRepository()
category_repository = CategoryRepository()

class ValueTest(BaseTest):

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

            cat = CategoryModel(
                libelle = "cabane dans les arbres", 
                show = True, 
            )
            
            category_repository.save(cat)
            category_repository.commit()
            
            prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi",
            is_required= True,
            category_id=1,
            )

            property_repository.save(prop)
            property_repository.commit()

            val = ValueModel(
            libelle="Active",
            property_id = 1,
            user_id = 1,
            )

            value_repository.save(val)
            value_repository.commit()
           
            self.assertIsNotNone(value_repository.get_value_by_id(1), "Did not find a value with id 1 after saving to db")

            value_repository.delete(val)
            value_repository.commit()
            self.assertEqual(len(value_repository.get_all()), 0)
