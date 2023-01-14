from app.categories.models import CategoryModel
from app.categories.repository import CategoryRepository
from tests.base_test import BaseTest


category_repository = CategoryRepository()

class CategoryTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():
            cat = CategoryModel(libelle="category test", show=True)

            category_repository.save(cat)
            category_repository.commit()

            self.assertIsNotNone(category_repository.get_category_by_id(1), "Did not find a category with id 'category test' after save_to_db")

            category_repository.delete(cat)
            category_repository.commit()
            self.assertEqual(len(category_repository.get_all()), 0)

            