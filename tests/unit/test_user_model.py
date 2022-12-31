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
    
    def test_create_user_withoutemail(self):
        user = UserModel(
                name = "MOTO",
                firstname = "Julien" ,
                username = "juju",
                phone_number = "+33 06 45 96 32 45",
                password = "12345",
                is_custom = True,
                is_owner = False,
                is_admin = False,
                birth_date = "13/08/1908",
                gender = True,
                is_activated = True
            )
        self.assertIsNone(user.email)