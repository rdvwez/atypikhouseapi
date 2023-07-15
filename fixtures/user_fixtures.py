import os, random
from faker import Faker

from passlib.hash import pbkdf2_sha256
from app.users.models import UserModel
from app.users.service import UserService
from app.images.models import ImageModel
from app.images.service import ImageService

class UserFixtures:
    def __init__(self) -> None:
        self.fake = Faker(locale='fr_FR')
        self.image_service = ImageService()
        self.roles = ("admin", "user","owner" )
        self.user_service = UserService()
        self.avatr_path = "https://xsgames.co/randomusers/avatar.php?g={}"
    
    def load(self) -> None:
        counter = 1
        for role in self.roles:

            if role == "admin":

                gender = 1
            
                lambda_name = "Doe"
                lambda_first_name = "Jhon"

                lambda_email = f"{lambda_first_name}.{lambda_name[0]}@hatypikhouse.fr"
            else:
                gender = self.fake.boolean(chance_of_getting_true=50)

                if gender:
                    lambda_name = self.fake.last_name_male(), 
                    lambda_first_name = self.fake.first_name_male()
                    
                else:
                    lambda_name = self.fake.last_name_female(), 
                    lambda_first_name = self.fake.first_name_female()
                    

                lambda_email = f"{lambda_first_name}.{lambda_name[0]}@hatypikhouse.fr"   

            user = UserModel(
                name = lambda_name,
                firstname = lambda_first_name ,
                username = lambda_name,
                phone_number = self.fake.phone_number(),
                email = lambda_email,
                password = pbkdf2_sha256.hash("password"),
                is_customer = True if role == "user" else False,
                is_owner = True if role == "owner" else False,
                is_admin = True if role == "admin" else False,
                birth_date = self.fake.date_of_birth(),
                gender = self.fake.boolean(chance_of_getting_true=50)
            )

            self.user_service.create_user(user)

            basename=self.fake.file_name(category="image")
            avavtar = ImageModel(
                                path= self.avatr_path.format('male') if role == "user" else self.avatr_path.format('female'), 
                                basename=basename,
                                is_avatar = True,
                                extension=os.path.splitext(basename)[1], 
                                user_id=counter)
            self.image_service.create_image_for_fixtures(avavtar)

                
            counter +=1
