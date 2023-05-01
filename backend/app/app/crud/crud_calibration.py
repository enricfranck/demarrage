from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.calibration import Calibration
from app.schemas.calibration import CalibrationCreate, CalibrationUpdate


class CRUDCalibration(CRUDBase[Calibration, CalibrationCreate, CalibrationUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Calibration]:
        return db.query(Calibration).filter(Calibration.uuid == uuid).first()

    
    def get_by_value(self, db: Session, *, value: str) -> Optional[Calibration]:
        return db.query(Calibration).filter(Calibration.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: CalibrationCreate
    ) -> Calibration:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


calibration = CRUDCalibration(Calibration)
