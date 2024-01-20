from faker import Faker

# from app.categories.service import CategoryService
from app.categories.models import CategoryModel
from app.categories.repository import CategoryRepository

# fake = Faker(locale='fr_FR')

class  CategoryFixtures:

    def __init__(self) -> None:
        self.categories_wordings = ["cabane dans les arbres", 
                                    "bulle", 
                                    "cabane sur l'eau", 
                                    "cabane",
                                    "cabana sur pilotis", 
                                    "chalet",  
                                    "lov'nid", 
                                    "roulotte", 
                                    "cabane de trappeur",
                                    "mirador", 
                                    "phare", 
                                    "maison de hobbit", 
                                    "yourte",
                                    "tini house", 
                                    "cabane verticale", 
                                    "tipi", 
                                    "bateau", 
                                    "igloo"]

        self.fake = Faker(locale='fr_FR')
        # self.category_service = CategoryService()
        self.category_repository = CategoryRepository()


    def load(self) -> None:
        
        for wording in self.categories_wordings:
            category = CategoryModel(libelle = wording, show = self.fake.boolean(chance_of_getting_true=50))
            self.category_repository.save(category)
            self.category_repository.commit()