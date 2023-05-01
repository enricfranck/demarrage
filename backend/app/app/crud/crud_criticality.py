from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.criticality import Criticality
from app.schemas.criticality import CriticalityCreate, CriticalityUpdate


class CRUDCriticality(CRUDBase[Criticality, CriticalityCreate, CriticalityUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Criticality]:
        return db.query(Criticality).filter(Criticality.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, value: str) -> Optional[Criticality]:
        return db.query(Criticality).filter(Criticality.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: CriticalityCreate
    ) -> Criticality:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


criticality = CRUDCriticality(Criticality)
