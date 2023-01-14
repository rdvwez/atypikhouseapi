from app.categories.models import CategoryModel
from app.properties.models import PropertyModel
from app.categories.repository import CategoryRepository
from app.properties.repository import PropertyRepository
from tests.base_test import BaseTest


category_repository = CategoryRepository()
property_repository = PropertyRepository()

class PropertyTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():
            cat = CategoryModel(libelle="category test", show=True)

            category_repository.save(cat)
            category_repository.commit()

            prop = PropertyModel(
            libelle="wifi",
            description="Bon wifi par ici",
            is_required= True,
            category_id=1,
            )
            property_repository.save(prop)
            property_repository.commit()
            self.assertIsNotNone(property_repository.get_property_by_id(1), "Did not find a property with id 1 after saving to db")

            property_repository.delete(prop)
            property_repository.commit()
            self.assertEqual(len(property_repository.get_all()), 0)

            