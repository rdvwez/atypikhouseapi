import random
from faker import Faker

# from app.values.service import ValueService
from app.values.models import ValueModel
from app.values.repository import ValueRepository

class  ValueFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        # self.value_service = ValueService()
        self.value_repository = ValueRepository()


    def load(self) -> None:
        x = 0
        while x < 15:
            value = ValueModel(libelle =f"{self.fake.sentence(nb_words=2)}{x}"  , property_id = random.randint(1,10), user_id = random.randint(1,3))
            # self.value_service.create_value(value)
            self.value_repository.save(value)
            self.value_repository.commit()
            x+=1