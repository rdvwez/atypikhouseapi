import os
import traceback
from flask import abort, send_file
from typing import List, Dict, Union, Tuple, Literal
from requests import Response
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import get_jwt_identity
from werkzeug.datastructures import FileStorage

from app.libs import image_helper

from app.images.repository import ImageRepository
from app.images.models import ImageModel


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
        # return self.category_repository.get_category_by_id(category_id)
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

    def give_rigth_folder(self, house_id: Union[int, None], user_id:int = None):
        if house_id:
            return f"madias/user_{house_id}" , False
        else:
            if user_id:
                return f"avatars/user_{user_id}" , True
            else:
                return f"avatars/user_{self.user_id}" , True


    def create_image(self, image_data:Dict[str, FileStorage], house_id:int):

        """
        used to upload an image file
        It uses JWT to retrieve information and then saves the image to the user's folder
        if there is a filename conflict, it appends a numbers at the end
        """

        # user_id = get_jwt_identity()
        extension = image_helper.get_extension(image_data["image"])
        folder, is_avatar = self.give_rigth_folder(house_id)
            
        try:
            image_path = image_helper.save_image(image = image_data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            image = ImageModel(path= image_path, extension = extension, user_id = self.user_id, is_avatar=is_avatar, house_id=house_id, basename= basename)
            
            
            self.image_repository.save(image)
            self.image_repository.commit()
            return {"message": f"Image {basename} uploaded"}, 201

        except UploadNotAllowed:
            
            return {"image": f"Extension {extension} is not allowed."}, 400
    
    def create_image_for_fixtures(self, image:ImageModel):
        self.image_repository.save(image)
        self.image_repository.commit()

    def update_image(self, image_data:Dict[str, FileStorage], auther_arguments:Dict[str,None]):

        image = self.image_repository.get_image_by_id(auther_arguments.get("image_id"))

        folder, is_avatar = self.give_rigth_folder(auther_arguments.get("house_id"))

        image_path = image_helper.find_image_any_format(image.basename, folder)

        if image_path:
            try:
                os.remove(image_path)
            except:
                return {"message":  "Internal error: Image upload failed during the delation of the former image "}, 500
        

        try:
            extension = image_helper.get_extension(image_data["image"])
            image_path = image_helper.save_image(image = image_data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)

            image.path = image_path
            image.extension = extension
            image.basename = basename

            self.image_repository.save(image)
            self.image_repository.commit()
            return {"message":  "Image uploaded successfully: {image}"}, 200
            
        except UploadNotAllowed:
            extension = image_helper.get_extension(image_data["image"])
            return {"message":f"The extension '{extension}' is not allowed: "}, 400


    def delete_image(self, image_id:int):
        image = self.get_image_by_id(image_id)

        if not image_helper.is_filename_safe(image.basename):
            return {"massage": f"Illagal filename {image.basename} requested"}, 400
        
        try:
            os.remove(image.path)
            # folder, is_avatr = self.give_rigth_folder(image.house_id)
            self.image_repository.delete(image)
            self.image_repository.commit()
            return {"massage": f"Image '{image.basename}' deleted"}, 200
        except FileExistsError:
            return {"massage":f"image '{image.basename}' not found"}, 404
        except:
            traceback.print_exc()
            return {"massage":f"Internal error: Internal server errorè! Fail to delete image"}, 500

