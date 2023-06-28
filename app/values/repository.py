from typing import List

from app.db import db

from app.values.models import ValueModel

class ValueRepository:

    """Persistence of Value"""

    def get_all(self)-> List[ValueModel]:
        return ValueModel.query.order_by(ValueModel.id).all()
    
    def delete_all(self) -> None: # type: ignore
        ValueModel.query.delete()

    def get_value_by_id(self, Value_id: int) -> ValueModel:
        value = ValueModel.query.get_or_404(Value_id)
        return value
    
    def save(self, value: ValueModel)-> None:
        db.session.add(value)

    def delete(self, value: ValueModel)-> None:
        db.session.delete(value)

    def flush(self)-> None:
        db.session.flush()

    def commit(self)-> None:
        db.session.commit()

    def rollback(self)-> None:
        db.session.rolback()