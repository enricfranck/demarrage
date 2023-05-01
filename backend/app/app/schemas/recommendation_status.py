from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class RecommendationStatusBase(BaseModel):
    value: Optional[str] = None


# Properties to receive via API on creation
class RecommendationStatusCreate(RecommendationStatusBase):
    value: str


# Properties to receive via API on update
class RecommendationStatusUpdate(RecommendationStatusBase):
    value: Optional[str] = None


class RecommendationStatusInDBBase(RecommendationStatusBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class RecommendationStatus(RecommendationStatusInDBBase):
    pass


# Additional properties stored in DB
class RecommendationStatusInDB(RecommendationStatusInDBBase):
    pass
