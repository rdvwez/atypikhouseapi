import random
from faker import Faker

# from app.houses.service import HouseService
from app.houses.models import HouseModel
from app.houses.repository import HouseRepository


class  HouseFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        # self.house_service = HouseService()
        self.house_repository = HouseRepository()
        # self.bedroom_and_person_number = random.randint(1,4)


    def load(self) -> None:
        
        x = 0
        while x < 40:
            bedroom_and_person_number = random.randint(1,4)
            house = HouseModel(libelle = self.fake.word() + str(random.randint(1,18)),
                                description = self.fake.paragraph(nb_sentences=4) ,
                                category_id = random.randint(1,18),
                                bedroom_number = bedroom_and_person_number,
                                person_number = bedroom_and_person_number,
                                parking_distance = random.randint(100,200),
                                area = bedroom_and_person_number * 4, # bedroom_and_person_number * 4 mettre carré
                                water = self.fake.boolean(chance_of_getting_true=50),
                                power = self.fake.boolean(chance_of_getting_true=50),
                                price = random.randint(25,50),
                                latitude = self.fake.latitude(),
                                longitude = self.fake.longitude(),
                                thematic_id = random.randint(1,16),
                                user_id = random.randint(1,3),
                                address = self.fake.street_address(),
                                city = self.fake.city(),
                                country = self.fake.country())
            self.house_repository.save(house)
            self.house_repository.commit()
            x+=1
            