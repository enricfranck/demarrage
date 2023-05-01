from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.failure_progress import FailureProgress
from app.schemas.failure_progress import FailureProgressCreate, FailureProgressUpdate
from app.utils import decode_text


class CRUDFailureProgress(CRUDBase[FailureProgress, FailureProgressCreate, FailureProgressUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[FailureProgress]:
        return db.query(FailureProgress).filter(FailureProgress.uuid == uuid).first()

    
    def get_value(self, db: Session, *, value: str) -> Optional[FailureProgress]:
        return db.query(FailureProgress).filter(FailureProgress.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: FailureProgressCreate
    ) -> FailureProgress:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = FailureProgress(**obj_in_data, value=decode_text(obj_in.title))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


failure_progress = CRUDFailureProgress(FailureProgress)
