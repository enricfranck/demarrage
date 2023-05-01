from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate


class CRUDRecord(CRUDBase[Record, RecordCreate, RecordUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Record]:
        return db.query(Record).filter(Record.uuid == uuid).first()

    
    def get_title(self, db: Session, *, title: str) -> Optional[Record]:
        return db.query(Record).filter(Record.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: RecordCreate
    ) -> Record:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


record = CRUDRecord(Record)
