

from app.db import db

from app.thematics.models import ThematicModel

class ThematicRepository:

    """Persistence of thematics"""

    def get_all(self):
        return ThematicModel.query.order_by(ThematicModel.id).all()
    
    def delete_all(self) -> None: # type: ignore
        ThematicModel.query.delete()

    def get_thematic_by_id(self, thematic_id: int) -> ThematicModel:
        thematic = ThematicModel.query.get_or_404(thematic_id)
        return thematic
    
    def save(self, thematic: ThematicModel)-> None:
        db.session.add(thematic)

    def delete(self, thematic: ThematicModel)-> None:
        db.session.delete(thematic)

    def flush(self)-> None:
        db.session.flush()

    def commit(self)-> None:
        db.session.commit()

    def rollback(self)-> None:
        db.session.rolback()