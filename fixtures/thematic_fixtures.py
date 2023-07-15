from faker import Faker

# from app.thematics.service import ThematicService
from app.thematics.models import ThematicModel
from app.thematics.repository import ThematicRepository

# fake = Faker(locale='fr_FR')

class  ThematicFixtures:

    def __init__(self) -> None:
        self.thematics_wordings = [ "romantique", "spa privatif", "familial", "retour à la natures", "extraordinnaire",  
            "ecologique", "vélo", "animaux bienvenus","< 100 € ", "clampig", "luxe", "amateur de vin",
            "Pêche", "observatoire des étoiles", "montagne", "à la ferme"]

        self.fake = Faker(locale='fr_FR')
        # self.thematic_service = ThematicService()
        self.thematic_repository = ThematicRepository()


    def load(self) -> None:
        
        for wording in self.thematics_wordings:
            thematic = ThematicModel(libelle = wording, show = self.fake.boolean(chance_of_getting_true=50))
            # self.thematic_service.create_thematic(thematic)
            self.thematic_repository.save(thematic)
            self.thematic_repository.commit()