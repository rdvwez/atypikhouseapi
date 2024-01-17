

from app.db import db
from typing import List

from app.properties.models import PropertyModel

class PropertyRepository:

    """Persistence of property"""

    def get_all(self):
        return PropertyModel.query.order_by(PropertyModel.id).all()
    
    def delete_all(self) -> None:
        PropertyModel.query.delete()

    def get_property_by_id(self, property_id: int) -> PropertyModel:
        property_object = PropertyModel.query.get_or_404(property_id)
        return property_object
    
    def get_properties_by_category_id(self, category_id: int)->List[PropertyModel]:
         return PropertyModel.query.filter(PropertyModel.category_id == category_id).all()

    def save(self, property_object):
        db.session.add(property_object)

    def delete(self, property_object):
        db.session.delete(property_object)

    def flush(self):
        db.session.flush()

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rolback()