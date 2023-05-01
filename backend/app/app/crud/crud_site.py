from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate
from app.utils import decode_text


class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Site]:
        return db.query(Site).filter(Site.uuid == uuid).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Site]:
        return db.query(Site).filter(Site.name == name).first()
        
    def create(
        self, db: Session, *, obj_in: SiteCreate
    ) -> Site:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Site(**obj_in_data, value=decode_text(obj_in.name))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


site = CRUDSite(Site)
