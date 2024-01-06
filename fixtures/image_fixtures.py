import os
import random
from faker import Faker

from app.images.models import ImageModel
from app.images.service import ImageService
from app.houses.repository import HouseRepository

IMAGES_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'atypikhouse_images'))
# IMAGES_FOLDER_PATH = "static/images/atypikhouse_images/bateau/bateau1.jpg"

IMAGES_FOLDER = { 
    1:"cabane_dans_arbre",
    2:"bulle",
    3:"cabane_sur_eau",
    4:"cabane",
    5:"cabane_sur_pilotis",
    6:"challet",
    7:"lovnid",
    8:"roulotte",
    9:"cabane_trappeur",
    10:"mirador",
    11:"phare",
    12:"maison_hobbit",
    13:"yourte",
    14:"tini_house",
    15:"cabane_verticale",
    16:"tipi",
    17:"bateu",
    18:"igloo"
    }

class  ImageFixtures:

    def __init__(self) -> None:

        self.fake = Faker(locale='fr_FR')
        self.image_service = ImageService()
        self.house_repository = HouseRepository()


    def load(self) -> None:
        # pass
        houses = self.house_repository.get_all()
        # house_counter = 1
        for house in houses:
            images_folder =  f"{IMAGES_FOLDER_PATH}/{IMAGES_FOLDER.get(house.category_id, 'standard')}"
            if os.path.exists(images_folder):

                # Liste de fichiers dans le dossier
                image_in_folder = os.listdir(images_folder)

                # Filtrer les fichiers pour ne prendre que ceux avec une extension d'image
                images = [image for image in image_in_folder if image.lower().endswith(('.jpg', '.jpeg', '.png'))]

                # Créer les URLs des images en fonction des chemins
                images_urls = [os.path.join(images_folder, image).replace('/app', '') for image in images]

                for image_url in images_urls:
                    basename = os.path.basename(image_url)
                    image = ImageModel(
                                    path= image_url, 
                                    is_avatar = False,
                                    basename=basename,
                                    extension=os.path.splitext(basename)[1],
                                    type_mime = "image/jpeg",
                                    size = random.randint(150,10000) ,
                                    user_id=house.user_id, 
                                    house_id= house.id)

                    self.image_service.create_image_for_fixtures(image)

