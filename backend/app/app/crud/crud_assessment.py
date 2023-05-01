from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate


class CRUDAssessment(CRUDBase[Assessment, AssessmentCreate, AssessmentUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Assessment]:
        return db.query(Assessment).filter(Assessment.uuid == uuid).first()

    def get_by_record(self, db: Session, *, record_id: UUID) -> Optional[Assessment]:
        return db.query(Assessment).filter(Assessment.record_id == record_id).first()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Assessment]:
        return db.query(Assessment).filter(Assessment.name == name).first()
        
    def create(
        self, db: Session, *, obj_in: AssessmentCreate
    ) -> Assessment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


assessment = CRUDAssessment(Assessment)
