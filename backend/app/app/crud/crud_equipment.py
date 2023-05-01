from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class CRUDEquipment(CRUDBase[Equipment, EquipmentCreate, EquipmentUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Equipment]:
        return db.query(Equipment).filter(Equipment.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[Equipment]:
        return db.query(Equipment).filter(Equipment.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: EquipmentCreate
    ) -> Equipment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


equipment = CRUDEquipment(Equipment)
