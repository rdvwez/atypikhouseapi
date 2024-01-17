import os
import random
from faker import Faker
import logging

# from app.houses.service import HouseService
from app.houses.models import HouseModel
from app.images.models import ImageModel
from app.houses.repository import HouseRepository
from app.images.service import ImageService

# IMAGES_FOLDER_PATH = "app/static/images/atypikhouse_images"
IMAGES_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'atypikhouse_images'))
# IMAGES_FOLDER_PATH = "static/images/atypikhouse_images/bateau/bateau1.jpg"


class  HouseFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        self.house_repository = HouseRepository()
        self.image_service = ImageService()


    def load(self) -> None:
        x = 0
        while x < 40:
            bedroom_and_person_number = random.randint(1,4)
            category_id = random.randint(1,18),
            house = HouseModel(libelle =f"{self.fake.word()}{random.randint(1,18)}{x}",
                                description = self.fake.paragraph(nb_sentences=4) ,
                                show = self.fake.boolean(chance_of_getting_true=50),
                                category_id = category_id,
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
                                user_id = random.randint(1,2),
                                address = self.fake.street_address(),
                                city = self.fake.city(),
                                country = self.fake.country())
            self.house_repository.save(house)
            self.house_repository.commit()
                
            x+=1
            