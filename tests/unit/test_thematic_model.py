from unittest import TestCase
from app.thematics.models import ThematicModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel


class ThematicTest(TestCase):

    def test_create_thematic(self):
        them = ThematicModel(
            libelle="romantiques", 
            show=True)

        self.assertEqual(True,them.show)
        self.assertEqual("romantiques", them.libelle)

    def test_create_thematic_without_libelle(self):
        them = ThematicModel( show=True)

        self.assertEqual(them.libelle, None)

    def test_create_thematic_with_libelle_to_long(self):
        them = ThematicModel( 
            libelle="""
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                """, 
            show=True)

        self.assertLess(40,len(them.libelle))

    def test_repr(self):
        them = ThematicModel(libelle="romantiques", show=True)
        thematic_dict_representation = them.__repr__()
        self.assertEqual(thematic_dict_representation, "{'id': None, 'libelle':'romantiques', 'show':True}")


    def test_create_thematic_Displayable(self):
        them = ThematicModel(
            id=1,
            libelle="romantiques", 
            show=True
        )

        self.assertTrue(them.show)

    def test_create_thematic_not_Displayable(self):
        them = ThematicModel(
            id=1,
            libelle="romantiques", 
            show=False
        )

        self.assertFalse(them.show)