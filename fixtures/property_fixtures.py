import random
from faker import Faker

from app.properties.service import PropertyService
from app.properties.models import PropertyModel


class  PropertyFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        self.property_service = PropertyService()


    def load(self) -> None:
        
        x = 0
        while x < 10:
            property_object = PropertyModel(libelle = self.fake.sentence(nb_words=2), 
                                    is_required = self.fake.boolean(chance_of_getting_true=50),
                                    description = self.fake.text(max_nb_chars=80) ,
                                    category_id = random.randint(1,18))
            self.property_service.create_property(property_object)
            x+=1
            