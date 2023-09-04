import os
import traceback
from flask import abort, send_file
from typing import List, Dict, Union, Tuple, Literal, Mapping
from requests import Response
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
# from flask_uploads import UploadNotAllowed
from flask_jwt_extended import get_jwt_identity
from werkzeug.datastructures import FileStorage


from app.libs import image_helper

from app.images.repository import ImageRepository
from app.images.models import ImageModel


FOLDER = 'madias'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class ImageService:

    @inject
    def __init__(self):
        self.image_repository = ImageRepository()
        # self.user_id = get_jwt_identity()


    def get_all_images(self):
        """
        Return all images
        :return: a list of Images objects
        """
        return self.image_repository.get_all()

    def get_image_by_id(self, image_id: int) -> ImageModel:
        return self.image_repository.get_image_by_id(image_id)
    
    # def get_image_by_name(self, image_name: str):
    #     """
    #     Returns the requested image if it exists. Looks up inside the logged in user's folder
    #     """
    #     # user_id = get_jwt_identity() 
    #     folder = f"user_{self.user_id }"
    #     if not image_helper.is_filename_safe(image_name):

    #         return {"massage": f"Illagal filename {image_name} requested"}, 400
        
    #     try:
    #         return send_file(image_helper.get_path(image_name, folder=folder))
    #     except FileNotFoundError:
    #         return {"massage":f"image '{image_helper}' not found"}, 404

    def give_rigth_folder(self, user_id:int, house_id:int)->Tuple[str, bool]:
        if house_id > 0:
            return f"madias/house_{house_id}", False
        else:
            return f"avatars/user_{user_id}", True
        # else:
        #     if user_id:
        #         return f"avatars/user_{user_id}" , True
        #     else: #update de la photo de profile de l'utilisateur courrent
        #         current_user_id = get_jwt_identity() 
        #         return f"avatars/user_{current_user_id}" , True

    def create_image(self, image:ImageModel)->ImageModel:
        self.image_repository.save(image)
        self.image_repository.commit()

        return image

        # """
        # used to upload an image file
        # It uses JWT to retrieve information and then saves the image to the user's folder
        # if there is a filename conflict, it appends a numbers at the end
        # """

        # user_id = get_jwt_identity()
        # extension = image_helper.get_extension(image_data["image"])
        # folder, is_avatar = self.give_rigth_folder(house_id)
            
        # try:
        #     image_path = image_helper.save_image(image = image_data["image"], folder=folder)
        #     basename = image_helper.get_basename(image_path)
        #     image = ImageModel(path= image_path, extension = extension, user_id = self.user_id, is_avatar=is_avatar, house_id=house_id, basename= basename)
            
            
        #     self.image_repository.save(image)
        #     self.image_repository.commit()
        #     return {"message": f"Image {basename} uploaded"}, 201

        # except UploadNotAllowed:
            
        #     return {"image": f"Extension {extension} is not allowed."}, 400

    def upload_image(self, image_file: FileStorage ):

        """
        used to upload an image file
        It uses JWT to retrieve information and then saves the image to the user's folder
        if there is a filename conflict, it appends a numbers at the end
        """
        

        if image_file.content_length > MAX_CONTENT_LENGTH:
            abort(413, 'The file is too large')
        
    
        extension = image_helper.get_extension(image_file)
            
        try:

                image_path = image_helper.save_image(image = image_file, folder=FOLDER)
                basename = image_helper.get_basename(image_path)
                
                current_user = get_jwt_identity()
                image = ImageModel(
                    path = image_path,
                    extension = extension,
                    basename = basename,
                    type_mime = image_file.content_type,
                    size = image_file.content_length ,
                    # house_id= image_data["house_id"],
                    user_id = current_user,
                    # is_avatar= is_avatar
                )

                self.image_repository.save(image)
                self.image_repository.commit()

                return image, 201

        except Exception as e:
            return {"image": f"Extension {extension} is not allowed."}, 400
    
    def create_image_for_fixtures(self, image:ImageModel):
        self.image_repository.save(image)
        self.image_repository.commit()

    def update_image(self, updated_image_data:dict, image_id:int)-> Tuple[ImageModel, Literal[200]]:
        try:
            image = self.image_repository.get_image_by_id(image_id)
            for key, value in updated_image_data.items():
                if hasattr(image, key):
                    setattr(image, key, value)

            self.image_repository.save(image)
            self.image_repository.commit()

            return image, 200
        except:
                abort(404, f"An Image with id:{image_id} doesn't exist")


    def delete_image(self, image_id:int):
        image = self.image_repository.get_image_by_id(image_id)
       
        if not image_helper.is_filename_safe(image.basename):
            return {"massage": f"Illegal filename {image.basename} requested"}, 400
        
        try:
            os.remove(image.path)
            self.image_repository.delete(image)
            self.image_repository.commit()
            return {"massage": f"Image '{image.basename}' has been deleted"}, 204
        except FileExistsError:
            return {"massage":f"image '{image.basename}' not found"}, 404
        except:
            traceback.print_exc()
            return {"massage":f"Internal server error: Fail to delete image"}, 500

