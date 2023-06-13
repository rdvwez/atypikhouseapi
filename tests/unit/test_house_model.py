from unittest import TestCase
from app.categories.models import CategoryModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel
from app.users.models import UserModel
from app.thematics.models import ThematicModel

class HouseTest(TestCase):

    def test_create_house(self):
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
            )
        
        self.assertEqual("libelle",house.libelle)
        self.assertEqual("description de la house",house.description)
        self.assertEqual(2,house.bedroom_number)
        self.assertEqual(2,house.person_number)
        self.assertEqual(12,house.parking_distance)
        self.assertEqual("44 rue des vaujours",house.address)
        self.assertEqual("paris",house.city)
        self.assertEqual("france",house.country)
        self.assertEqual(12,house.area)
        self.assertEqual(True,house.water)
        self.assertEqual(True,house.power)
        self.assertEqual(24,house.price)
        self.assertEqual(13.008795,house.latitude)
        self.assertEqual(58.25669,house.longitude)

    def test_repr(self):
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
            )
        
        house_dict_representation = house.__repr__()
        del house_dict_representation["_sa_instance_state"]
        self.assertEqual(house_dict_representation, { "libelle" : "libelle",
                                                    "description" : "description de la house",
                                                    "bedroom_number" : 2,
                                                    "person_number" : 2,
                                                    "parking_distance" : 12,
                                                    "address" : "44 rue des vaujours",
                                                    "city" : "paris",
                                                    "country" : "france",
                                                    "area" : 12,
                                                    "water" : True,
                                                    "power" : True,
                                                    "price" : 24,
                                                    "latitude" : 13.008795,
                                                    "longitude" : 58.25669,
                                                    })

    def test_create_house_without_libelle(self):
        house = HouseModel(
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            area = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.libelle)

    def test_create_house_without_bedroom_number(self):
        house = HouseModel(
            libelle = "libelle",
            person_number = 2,
            parking_distance = 12,
            area = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.bedroom_number)
    
    def test_create_house_without_person_number(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            parking_distance = 12,
            area = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.person_number)
    
    def test_create_house_without_parking_distance(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            area = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.parking_distance)

    def test_create_house_without_area(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.area)
    
    def test_create_house_without_water(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = False,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertFalse(house.water)

    def test_create_house_without_power(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = False,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertFalse(house.power)
    
    def test_create_house_with_power(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertTrue(house.power)
    
    def test_create_house_with_water(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertTrue(house.water)
    
    def test_create_house_without_price(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            latitude = 13.008795,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.price)

    def test_create_house_without_latitude(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            price = 24,
            longitude = 58.25669,
            )
        
        self.assertIsNone(house.latitude)

    def test_create_house_without_longitude(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = 2,
            person_number = 2,
            parking_distance = 12,
            water = True,
            power = True,
            price = 24,
            latitude = 13.008795,
            )
        
        self.assertIsNone(house.longitude)

    def test_create_house_without_wrong_column_type(self):
        house = HouseModel(
            libelle = "libelle",
            bedroom_number = '2',
            person_number = '2',
            parking_distance = '12',
            water = True,
            power = True,
            price = '24',
            latitude = '13.008795',
            longitude = '58.25669',
            )
        
        self.assertNotEqual(type(house.longitude), "<class 'float'>")
        self.assertNotEqual(type(house.latitude), "<class 'float'>")
        self.assertNotEqual(type(house.bedroom_number), "<class 'int'>")
        self.assertNotEqual(type(house.person_number), "<class 'int'>")
        self.assertNotEqual(type(house.parking_distance), "<class 'int'>")
        self.assertNotEqual(type(house.price), "<class 'int'>")

    def test_house_owner(self):
        user = UserModel(
            id=1,
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_customer = True,
            is_owner = False,
            is_admin = False,
        )

        cat = CategoryModel(
            id=1,
            libelle = "cabane dans les arbres", 
            show = True, 
        )

        them = ThematicModel(
            id=1,
            libelle="romantiques", 
            show=False
        )

        img = ImageModel(
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = False
            )

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
            user_id = 1,
            user = user,
            category_id = 1,
            category = cat,
            thematic_id = 1,
            thematic = them,
            images= [img]
            )
        
        self.assertEqual(house.__repr__().get("user_id"), user.id)
        self.assertEqual(house.__repr__().get("category_id"), cat.id)
        self.assertEqual(house.__repr__().get("thematic_id"), them.id)
        self.assertTrue(house.__repr__().get("images"))

        
        
