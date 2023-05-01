from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.risk import Risk
from app.schemas.risk import RiskCreate, RiskUpdate


class CRUDRisk(CRUDBase[Risk, RiskCreate, RiskUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Risk]:
        return db.query(Risk).filter(Risk.uuid == uuid).first()

    
    def get_by_value(self, db: Session, *, value: str) -> Optional[Risk]:
        return db.query(Risk).filter(Risk.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: RiskCreate
    ) -> Risk:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


risk = CRUDRisk(Risk)
