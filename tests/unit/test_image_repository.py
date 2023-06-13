from app.houses.models import HouseModel
from app.users.models import UserModel
from app.categories.models import CategoryModel
from app.thematics.models import ThematicModel
from app.images.models import ImageModel
from app.houses.repository import HouseRepository
from app.categories.repository import CategoryRepository
from app.thematics.repository import ThematicRepository
from app.images.repository import ImageRepository
from app.users.repository import UserRepository
from tests.base_test import BaseTest




category_repository = CategoryRepository()
house_repository = HouseRepository()
thematic_repository = ThematicRepository()
user_repository = UserRepository()
image_repository = ImageRepository()

class ImageTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():

            user = UserModel(
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_customer = True,
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

            img = ImageModel(
            path = "/images/madia/",
            extension = ".pjpg",
            basename = "paysage.jpg",
            is_avatar = False,
            house_id = 1,
            user_id = 1
            )

            image_repository.save(img)
            image_repository.commit()

            self.assertIsNotNone(image_repository.get_image_by_id(1), "Did not find a image with id 1 after saving to db")

            house_repository.delete(img)
            house_repository.commit()
            self.assertEqual(len(image_repository.get_all()), 0)

            