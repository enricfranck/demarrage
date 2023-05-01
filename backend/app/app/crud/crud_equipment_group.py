from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.equipment_group import EquipmentGroup
from app.schemas.equipment_group import EquipmentGroupCreate, EquipmentGroupUpdate
from app.utils import decode_text


class CRUDEquipmentGroup(CRUDBase[EquipmentGroup, EquipmentGroupCreate, EquipmentGroupUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[EquipmentGroup]:
        return db.query(EquipmentGroup).filter(EquipmentGroup.uuid == uuid).first()

    
    def get_by_value(self, db: Session, *, value: str) -> Optional[EquipmentGroup]:
        return db.query(EquipmentGroup).filter(EquipmentGroup.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: EquipmentGroupCreate
    ) -> EquipmentGroup:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = EquipmentGroup(**obj_in_data, value=decode_text(obj_in.title))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


equipment_group = CRUDEquipmentGroup(EquipmentGroup)
