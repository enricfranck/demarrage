from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.utils import decode_text


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Company]:
        return db.query(Company).filter(Company.uuid == uuid).first()

    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Company]:
        return db.query(Company).filter(Company.name == name).first()
        
    def create(
        self, db: Session, *, obj_in: CompanyCreate
    ) -> Company:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Company(**obj_in_data, value=decode_text(obj_in.name))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


company = CRUDCompany(Company)
