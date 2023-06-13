import os
import random
from faker import Faker

from app.images.models import ImageModel
from app.images.service import ImageService

END_POINT = "https://api.unsplash.com/photos/?client_id=YOUR_ACCESS_KEY"

class  ImageFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        self.image_service = ImageService()
        self.path = "https://api.lorem.space/image/house?w={}&h={}"


    def load(self) -> None:
        house_counter = 1
        while house_counter < 40:
            image_counter =0
            while image_counter < 3:
                basename=self.fake.file_name(category="image")
                image = ImageModel(
                                path= self.path.format(random.randint(150,220),random.randint(150,200)), 
                                basename=basename,
                                extension=os.path.splitext(basename)[1],
                                type_mime = "image/jpeg",
                                size = random.randint(150,10000) ,
                                user_id=random.randint(2,3), 
                                house_id= house_counter)

                self.image_service.create_image_for_fixtures(image)
                image_counter+=1
            house_counter+=1