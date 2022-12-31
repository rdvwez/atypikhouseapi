from unittest import TestCase
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel
from app.users.models import UserModel


class ValueTest(TestCase):

    def test_create_value(self):
        val = ValueModel(libelle="Active")
        self.assertEqual('Active',val.libelle)

    def test_repr(self):
        val = ValueModel(libelle="Active")
        value_dict_representation = val.__repr__()
        del value_dict_representation["_sa_instance_state"]
        self.assertEqual(value_dict_representation, {"libelle":"Active"})

    def test_property_value(self):
        prop = PropertyModel(
            id=1,
            libelle="wifi",
            description="Bon wifi",
            is_required= True,
            category_id=1,
        )

        val = ValueModel(
            id=1,
            libelle="Active",
            property_id = 1,
            property_object = prop
            )

        self.assertEqual(val.__repr__().get("property_id"), prop.id)

    def test_user_value(self):

        user = UserModel(
            id=1,
            email = "toto@gmail.com",
            password = "Le_passe_de_test",
            is_custom = True,
            is_owner = False,
            is_admin = False,
        )

        val = ValueModel(
            id=1,
            libelle="Active",
            user_id = 1,
            user = user
            )

        self.assertEqual(val.__repr__().get("user_id"), user.id)