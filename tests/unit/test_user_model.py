import re
from unittest import TestCase
from app.categories.models import CategoryModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel
from app.users.models import UserModel


class UserTest(TestCase):

    def test_create_user(self):

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
                birth_date = "13/08/1908",
                gender = True,
                is_activated = True
            )
        
        self.assertEqual(user.name,"MOTO")
        self.assertEqual(user.firstname,"Julien")
        self.assertEqual(user.username,"juju")
        self.assertEqual(user.phone_number,"+33 06 45 96 32 45")
        self.assertEqual(user.password,"12345")
        self.assertEqual(user.birth_date,"13/08/1908")
        self.assertTrue(user.is_custom)
        self.assertFalse(user.is_owner)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.gender)
        self.assertTrue(user.is_activated)
    
    def test_repr(self):
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
                birth_date = "13/08/1908",
                gender = True,
                is_activated = True
            )
        user_dict_representation = user.__repr__()
        del user_dict_representation["_sa_instance_state"]
        self.assertEqual(user_dict_representation, {"name":"MOTO", 
                                                    "firstname":"Julien",
                                                    "username":"juju",
                                                    "phone_number": "+33 06 45 96 32 45",
                                                    "email":"julien.moto@gmail.com",
                                                    "password":"12345",
                                                    "is_custom" : True,
                                                    "is_owner" : False,
                                                    "is_admin" : False,
                                                    "birth_date" : "13/08/1908",
                                                    "gender" : True,
                                                    "is_activated" : True
                                                    })
    
    def test_create_user_without_email(self):
        user = UserModel( password = "12345" )

        self.assertIsNone(user.email)
    
    def test_create_user_with_wrong_email_format(self):
        user = UserModel(
                email = "julien.motogmail.com",
                password = "12345",
            )
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        self.assertFalse(re.fullmatch(regex, user.email))

    def test_create_user_with_good_email_format(self):
        user = UserModel(
                email = "julien.moto@gmail.com",
                password = "12345",
            )
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        self.assertTrue(re.fullmatch(regex, user.email))
    
    def test_create_user_without_password_format(self):
        user = UserModel( email = "julien.moto@gmail.com",  )
        
        self.assertIsNone(user.password)
    
    def test_create_user_with_password_too_long(self):
        user = UserModel( email = "julien.moto@gmail.com", 
                         password = """ in voluptate velit esse orem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                                        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                                        consequat. Duis aute irure dolor in reprehenderit """,
                          )
        
        self.assertLess(255,len(user.password))

    def test_create_admin_user(self):
        user = UserModel(
                email = "julien.moto@gmail.com",
                password = "12345",
                is_admin = True,
            )
        
        self.assertTrue(user.is_admin)
    
    def test_create_owner_user(self):
        user = UserModel(
                email = "julien.moto@gmail.com",
                password = "12345",
                is_owner = True,
            )
        
        self.assertTrue(user.is_owner)

    def test_create_custom_user(self):
        user = UserModel(
                email = "julien.moto@gmail.com",
                password = "12345",
                is_custom = True,
            )
        
        self.assertTrue(user.is_custom)

    def test_create_user_with_houses(self):
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

        user = UserModel(
                id = 1,
                email = "julien.moto@gmail.com",
                password = "12345",
                houses = [house]
            )
        
        self.assertEqual(user.__repr__().get("houses"), True)

    def test_create_user_with_values(self):
        val = ValueModel(
            id=1,
            libelle="Active",
            )

        user = UserModel(
                id = 1,
                email = "julien.moto@gmail.com",
                password = "12345",
                values = [val]
            )
        
        self.assertEqual(user.__repr__().get("values"), True)

    def test_create_user_with_images(self):
        img = ImageModel(
            id=1,
            path = "/images/madia/",
            extension = ".jpg",
            basename = "paysage.jpg",
            is_avatar = True
            )

        user = UserModel(
                id = 1,
                email = "julien.moto@gmail.com",
                password = "12345",
                images = [img]
            )
        
        self.assertEqual(user.__repr__().get("images"), True)