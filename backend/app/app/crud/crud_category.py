from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Category]:
        return db.query(Category).filter(Category.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[Category]:
        return db.query(Category).filter(Category.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: CategoryCreate
    ) -> Category:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


category = CRUDCategory(Category)
