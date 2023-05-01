from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate
from app.utils import decode_text


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Team]:
        return db.query(Team).filter(Team.uuid == uuid).first()

    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Team]:
        return db.query(Team).filter(Team.name == name).first()
        
    def create(
        self, db: Session, *, obj_in: TeamCreate
    ) -> Team:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Team(**obj_in_data, value=decode_text(obj_in.name))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


team = CRUDTeam(Team)
