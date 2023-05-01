from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inspection_condition import InspectionCondition
from app.schemas.inspection_condition import InspectionConditionCreate, InspectionConditionUpdate
from app.utils import decode_text


class CRUDInspectionCondition(CRUDBase[InspectionCondition, InspectionConditionCreate, InspectionConditionUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[InspectionCondition]:
        return db.query(InspectionCondition).filter(InspectionCondition.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[InspectionCondition]:
        return db.query(InspectionCondition).filter(InspectionCondition.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: InspectionConditionCreate
    ) -> InspectionCondition:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = InspectionCondition(**obj_in_data, value=decode_text(obj_in.title))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inspection_condition = CRUDInspectionCondition(InspectionCondition)
