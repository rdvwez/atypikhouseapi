from faker import Faker

from app.categories.service import CategoryService
from app.categories.models import CategoryModel

# fake = Faker(locale='fr_FR')

class  CategoryFixtures:

    def __init__(self) -> None:
        self.categories_wordings = ["cabane dans les arbres", "bulle", "cabane sur l'eau", "cabane","cabana sur pilotis", "chalet",  
            "lov'nid", "roulotte", "cabane de trappeur","dôme", "maison troclodite", "maison de hobbit", "yourte",
            "tini house", "cabane verticale", "tipi", "bateau", "inclassable"]

        self.fake = Faker(locale='fr_FR')
        self.category_service = CategoryService()


    def load(self) -> None:
        
        for wording in self.categories_wordings:
            category = CategoryModel(libelle = wording, show = self.fake.boolean(chance_of_getting_true=50))
            self.category_service.create_category(category)