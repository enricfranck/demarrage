from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.defect import Defect
from app.schemas.defect import DefectCreate, DefectUpdate


class CRUDDefect(CRUDBase[Defect, DefectCreate, DefectUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Defect]:
        return db.query(Defect).filter(Defect.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[Defect]:
        return db.query(Defect).filter(Defect.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: DefectCreate
    ) -> Defect:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


defect = CRUDDefect(Defect)
