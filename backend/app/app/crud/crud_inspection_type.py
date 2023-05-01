from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inspection_type import InspectionType
from app.schemas.inspection_type import InspectionTypeCreate, InspectionTypeUpdate
from app.utils import decode_text


class CRUDInspectionType(CRUDBase[InspectionType, InspectionTypeCreate, InspectionTypeUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[InspectionType]:
        return db.query(InspectionType).filter(InspectionType.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[InspectionType]:
        return db.query(InspectionType).filter(InspectionType.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: InspectionTypeCreate
    ) -> InspectionType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = InspectionType(**obj_in_data, value=decode_text(obj_in.title))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inspection_type = CRUDInspectionType(InspectionType)
