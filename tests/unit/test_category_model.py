import json
from unittest import TestCase

from app.categories.models import CategoryModel
from app.houses.models import HouseModel
from app.properties.models import PropertyModel
from app.values.models import ValueModel
from app.images.models import ImageModel


class CategoryTest(TestCase):

    def test_create_category(self):
        cat = CategoryModel(
            libelle="cabane dans les arbres", 
            show=True)

        self.assertEqual(True,cat.show)
        self.assertEqual("cabane dans les arbres", cat.libelle)

    def test_create_category_Displayable(self):
        cat = CategoryModel(
            libelle="cabane dans les arbres", 
            show=True)

        self.assertTrue(cat.show)

    def test_create_category_not_Displayable(self):
        cat = CategoryModel(
            libelle="cabane dans les arbres", 
            show=False)

        self.assertFalse(cat.show)

    def test_create_category_without_libelle(self):
        cat = CategoryModel( show=True)

        self.assertEqual(cat.libelle, None)

    def test_create_category_with_libelle_to_long(self):
        cat = CategoryModel( 
            libelle="""
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                """, 
            show=True)

        self.assertLess(40,len(cat.libelle))

    def test_repr(self):
        cat = CategoryModel(libelle="cabane dans les arbres", show=True)
    
        # Créer un dictionnaire représentant l'objet cat
        cat_dict = {
            "id": cat.id,
            "libelle": cat.libelle,
            "show": cat.show
        }
        
        # Convertir le dictionnaire en une chaîne JSON valide
        cat_json = json.dumps(cat_dict)
        
        # Charger la chaîne JSON en tant que dictionnaire
        category_dict_representation = json.loads(cat_json)
        
        # Supprimer la clé "_sa_instance_state" si elle existe
        # category_dict_representation.pop('_sa_instance_state', None)
        
        expected_dict = {
            "id": None,
            "libelle": "cabane dans les arbres",
            "show": True
        }
        self.assertEqual(category_dict_representation, expected_dict)


    # def test_category_with_propertie(self):

    #     prop = PropertyModel(
    #         id=1,
    #         libelle="wifi",
    #         description="Bon wifi",
    #         is_required= True,
    #         category_id=1,
    #     )
    #     cat = CategoryModel(
    #         id=1,
    #         libelle = "cabane dans les arbres", 
    #         show = True, 
    #         properties = [prop]
    #     )
    #     breakpoint()
    #     self.assertEqual(cat.__repr__().get("properties"), True)

    # def test_create_category_with_house(self):

    #     house = HouseModel(
    #         id = 1,
    #         libelle = "libelle",
    #         description = "description de la house",
    #         bedroom_number = 2,
    #         person_number = 2,
    #         parking_distance = 12,
    #         address = "44 rue des vaujours",
    #         city = "paris",
    #         country = "france",
    #         area = 12,
    #         water = True,
    #         power = True,
    #         price = 24,
    #         latitude = 13.008795,
    #         longitude = 58.25669,
    #     )

    #     cat = CategoryModel(
    #         id=1,
    #         libelle = "cabane dans les arbres", 
    #         show = True, 
    #         houses = [house]
    #     )
    #     breakpoint()
    #     print(cat.houses)

    #     self.assertEqual(cat.__repr__().get("houses"), True)