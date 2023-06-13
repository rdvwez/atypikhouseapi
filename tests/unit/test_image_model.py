from unittest import TestCase
from app.categories.models import CategoryModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel
from app.users.models import UserModel

class ImageTest(TestCase):

    def test_create_image(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertEqual("/images/madia/",img.path)
        self.assertEqual(".jpg", img.extension)
        self.assertEqual("paysage.jpg", img.basename)
        self.assertEqual(False, img.is_avatar)

    def test_repr(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )
        image_dict_representation = img.__repr__()
        del image_dict_representation["_sa_instance_state"]
        self.assertEqual(image_dict_representation, {"path":"/images/madia/", 
                                                    "extension":".jpg",
                                                    "basename":"paysage.jpg",
                                                    "is_avatar":False
                                                    })

    def test_create_image_without_path(self):
        img = ImageModel(
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertIsNone(img.path)

    def test_create_image_without_extension(self):
        img = ImageModel(
            path = "/images/madia/",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertIsNone(img.extension)

    def test_create_image_without_basename(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            is_avatar = False
            )

        self.assertIsNone(img.basename)

    def test_create_image_without_is_avatar(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            )

        self.assertIsNone(img.is_avatar)

    def test_image_is_not_avatar(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )
        self.assertFalse(img.is_avatar)

    def test_image_is_avatar(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".png",
            basename = "avatar.png",
            is_avatar = True
            )
        self.assertTrue(img.is_avatar)

    def test_create_image_with_not_supported_extension(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".pdf",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertNotIn(img.extension, [".jpg",".png", ".jpeg",".gif"])

    def test_create_image_with_basename_to_long(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "Duis_aute_irure_dolor_inreprehenderit_in_voluptate_velit_esse_cillum_dolore_eu_fugiat_nulla_pariatur.jpg",
            is_avatar = False
            )

        self.assertLess(100,len(img.basename))

    def test_create_image_without_house(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertIsNone(img.house)

    def test_create_image_without_user(self):
        img = ImageModel(
            path = "/images/madia/",
            extension = ".pdf",
            basename = "paysage.jpg",
            is_avatar = False
            )

        self.assertIsNone(img.user)

    def test_create_image_with_user(self):
        user = UserModel(
            id=1,
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_customer = True,
            is_owner = False,
            is_admin = False,
        )

        img = ImageModel(
            path = "/images/madia/",
            extension = ".pdf",
            basename = "paysage.jpg",
            is_avatar = False,
            user_id = 1,
            user= user
            )

        self.assertEqual(img.__repr__().get("user_id"), user.id)

    def test_create_image_with_house(self):
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

        img = ImageModel(
            path = "/images/madia/",
            extension = ".pdf",
            basename = "paysage.jpg",
            is_avatar = False,
            house_id = 1,
            house= house
            )

        self.assertEqual(img.__repr__().get("house_id"), house.id)