from app.thematics.models import ThematicModel
from app.thematics.repository import ThematicRepository
from tests.base_test import BaseTest


thematic_repository = ThematicRepository()

class ThematicTest(BaseTest):

    def test_crud(self) -> None:

        with self.app_context():
            thematic = ThematicModel(libelle="thematic test", show=True)

            thematic_repository.save(thematic)
            thematic_repository.commit()

            self.assertIsNotNone(thematic_repository.get_thematic_by_id(1), "Did not find a thematic with id 'thematic test' after save_to_db")

            thematic_repository.delete(thematic)
            thematic_repository.commit()
            self.assertEqual(len(thematic_repository.get_all()), 0)

            