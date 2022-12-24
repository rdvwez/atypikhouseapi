from flask import request
from flask.views import MethodView
from flask_uploads import UploadNotAllowed
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.libs import image_helper
from app.images.service import ImageService
from app.images.models import ImageModel

from schemas import ImageSchema




blp = Blueprint("Images",__name__,description="Operations on images")


@blp.route("/image<string:image_id>")
class Image(MethodView):

    @inject
    def __init__(self):
        self.image_service = ImageService()
        self.image_schema = ImageSchema()

    @blp.response(200, ImageSchema)
    def get(self, image_id:int):
        """
        Returns the requested image if it exists. Looks up inside the logged in user's folder
        """
        return self.image_service.get_image_by_id(image_id)


    def delete(self, image_id:int):
        """
        Returns the Success deletion image
        """
        return self.image_service.delete_image(image_id)

    #TODO below
    # @blp.arguments(HouseUpdateSchema) 
    @blp.response(200, ImageSchema)
    def put(self):
        """
        This endpopint is used to upload an image. All avatars are na,ed after the user's ID.
        Something like this: user_{id} or house_{id}
        Uploading a new avatar overwrites the existing one.
        :return:
        """
        auther_arguments=request.form.get
        data = self.image_schema.load(request.files)
        return self.image_service.update_image(image_data= data, auther_arguments= auther_arguments)


@blp.route("/uploadimage/image")
class ImageUpload(MethodView):

    @inject
    def __init__(self):
        self.image_service = ImageService()
        self.image_schema = ImageSchema()

    @jwt_required
    @blp.arguments(ImageSchema)
    @blp.response(200, ImageSchema)
    def post(self):

        house_id=request.form.get('house_id', None)
        data = self.image_schema.load(request.files) #{"image":FileStorage}
        return self.image_service.create_image(image_data= data, house_id= house_id)
        # return category

        # image = ImageModel()


       

