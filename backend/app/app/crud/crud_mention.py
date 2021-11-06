from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.mention import Mention
from app.schemas.mention import MentionCreate, MentionUpdate


class CRUDMention(CRUDBase[Mention, MentionCreate, MentionUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Mention]:
        return db.query(Mention).filter(Mention.uuid == uuid).first()
        
    def create(
        self, db: Session, *, obj_in: MentionCreate
    ) -> Mention:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Mention]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )


mention = CRUDMention(Mention)
