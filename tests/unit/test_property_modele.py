from unittest import TestCase
from app.categories.models import CategoryModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel
from app.users.models import UserModel

class PropertyTest(TestCase):

    def test_create_peoperty(self):
        prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,
            )

        self.assertEqual(True,prop.is_required)
        self.assertEqual("wifi", prop.libelle)
        self.assertEqual("Bon wifi par ici", prop.description)

    def test_create_property_Displayable(self):
        prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,)

        self.assertTrue(prop.is_required)

    def test_create_property_not_Displayable(self):
        prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= False,)

        self.assertFalse(prop.is_required)

    def test_create_property_without_libelle(self):
        prop = PropertyModel(
            description="Bon wifi par ici",
            is_required= False,)
        
        self.assertEqual(prop.libelle, None)
    
    def test_create_property_with_libelle_to_long(self):
        prop = PropertyModel(
            libelle="""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam""",
            description="Bon wifi par ici",
            is_required= True,)

        self.assertLess(40,len(prop.libelle))

    def test_repr(self):
        prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,)
        property_dict_representation = prop.__repr__()
        del property_dict_representation["_sa_instance_state"]
        self.assertEqual(property_dict_representation, {"libelle":"wifi", "is_required":True, "description":"Bon wifi par ici"})
    
    def test_property_with_category(self):
        cat = CategoryModel(
            id=1,
            libelle = "cabane dans les arbres", 
            show = True, 
        )
        
        prop = PropertyModel(
            id=1,
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,
            category_id=1,
            )
        
        self.assertEqual(prop.category_id, cat.id)
    
    def test_property_without_category(self):

        prop = PropertyModel(
            id=1,
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,
            )
        
        self.assertIsNone(prop.category_id)

    def test_property_with_values(self):
        val = ValueModel(
            id=1,
            libelle="Active",
            property_id = 1,
            )
        
        prop = PropertyModel(
            id=1,
            libelle="wifi",
            description="Bon wifi par ici",
            values=[val]
            )
        
    
        self.assertEqual(prop.__repr__().get("values"), True)

    def test_property_without_values(self):
        
        prop = PropertyModel(
            id=1,
            libelle="wifi",
            description="Bon wifi par ici",
            )
        
    
        self.assertFalse(prop.__repr__().get("values"))