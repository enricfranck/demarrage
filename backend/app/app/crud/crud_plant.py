from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantUpdate
from app.utils import decode_text


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Plant]:
        return db.query(Plant).filter(Plant.uuid == uuid).first()

    
    def get_by_value(self, db: Session, *, value: str) -> Optional[Plant]:
        return db.query(Plant).filter(Plant.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: PlantCreate
    ) -> Plant:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Plant(**obj_in_data, value=decode_text(obj_in.title))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


plant = CRUDPlant(Plant)
