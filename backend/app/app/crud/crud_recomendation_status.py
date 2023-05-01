from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.recommendation_status import RecommendationStatus
from app.schemas.recommendation_status import RecommendationStatusCreate, RecommendationStatusUpdate


class CRUDRecommendationStatus(CRUDBase[RecommendationStatus, RecommendationStatusCreate, RecommendationStatusUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[RecommendationStatus]:
        return db.query(RecommendationStatus).filter(RecommendationStatus.uuid == uuid).first()

    
    def get_by_value(self, db: Session, *, value: str) -> Optional[RecommendationStatus]:
        return db.query(RecommendationStatus).filter(RecommendationStatus.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: RecommendationStatusCreate
    ) -> RecommendationStatus:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


recommendation_status = CRUDRecommendationStatus(RecommendationStatus)
