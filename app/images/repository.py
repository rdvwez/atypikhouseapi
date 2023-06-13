from typing import List

from app.db import db

from app.images.models import ImageModel

class ImageRepository:

    """Persistence of Images"""

    def get_all(self) -> List[ImageModel]:
        return ImageModel.query.order_by(ImageModel.id).all()

    def get_image_by_id(self, image_id: int) -> ImageModel:
        return ImageModel.query.get_or_404(image_id)
    
    def get_last_image(self) -> ImageModel:
        return ImageModel.query.order_by(ImageModel.id.desc()).first()
        
    
    def save(self, image: ImageModel) -> None:
        db.session.add(image)

    def delete(self, image: ImageModel) -> None:
        db.session.delete(image)

    def flush(self) -> None:
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rolback()