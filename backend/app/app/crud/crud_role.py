from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Role]:
        return db.query(Role).filter(Role.uuid == uuid).first()

    
    def get_title(self, db: Session, *, title: str) -> Optional[Role]:
        return db.query(Role).filter(Role.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: RoleCreate
    ) -> Role:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


role = CRUDRole(Role)
