from flask import request
from flask.views import MethodView
from flask_uploads import UploadNotAllowed
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import marshal

from app.libs import image_helper
from app.images.service import ImageService
from app.images.models import ImageModel
from app.libs.decorators import owner_required

from schemas import ImageSchema, PlainImageUpdateSchema, UploadImageSchema




blp = Blueprint("Images",__name__,description="Operations on images", url_prefix="/api")


@blp.route("/image/<string:image_id>")
class Image(MethodView):

    @inject
    def __init__(self):
        self.image_service = ImageService()
        self.image_schema = ImageSchema()

    @jwt_required()
    @blp.response(200, ImageSchema)
    def get(self, image_id:int):
        """
        Returns the requested image if it exists. Looks up inside the logged in user's folder
        """
        return self.image_service.get_image_by_id(image_id)

    @jwt_required()
    def delete(self, image_id:int):
        """
        Returns the Success deletion image
        """
        return self.image_service.delete_image(image_id)


    @jwt_required(fresh=True)
    @blp.arguments(PlainImageUpdateSchema) 
    @blp.response(200, ImageSchema)
    def put(self, *args, **kwargs):
        """
        This endpopint is used to upload an image.
        Uploading a new avatar overwrites the existing one.
        :return:
        """
        return self.image_service.update_image(updated_image_data=args[0] , image_id=kwargs.get("image_id"))


@blp.route("/uploadimage")
class ImageUpload(MethodView):

    @inject
    def __init__(self):
        self.image_service = ImageService()
        self.image_schema = UploadImageSchema()

    @jwt_required(fresh=True)
    @blp.arguments(UploadImageSchema)
    @blp.response(201, ImageSchema)
    def post(self,image_data ):
        if "image" not in request.files:
            return {"message":f"file is missing in your request "}, 400
        data = self.image_schema.load(request.files) #{"image":FileStorage}
        
        return self.image_service.upload_image(data.get("image"))
    
@blp.route("/image")
class ImageList(MethodView):

    @inject
    def __init__(self):
        self.image_service = ImageService()

    @blp.response(200, ImageSchema(many=True))
    def get(self):
        return self.image_service.get_all_images()

    # @jwt_required()
    # @blp.arguments(ImageSchema)
    # @blp.response(201, ImageSchema)
    # def post(self, image_data):
    #     image = ImageModel(**image_data)
    #     return self.image_service.create_image(image)


       

