from typing import List

from app.db import db

from app.categories.models import CategoryModel

class CategoryRepository:

    """Persistence of categories"""

    def get_all(self) -> List[CategoryModel]:
        return CategoryModel.query.order_by(CategoryModel.id).all()

    def get_category_by_id(self, category_id: int) -> CategoryModel:
        category = CategoryModel.query.get_or_404(category_id)
        return category
    
    def save(self, category: CategoryModel) -> None:
        db.session.add(category)

    def delete(self, category: CategoryModel) -> None:
        db.session.delete(category)

    def flush(self) -> None:
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rolback()