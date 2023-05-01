from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class AssessmentBase(BaseModel):
    status: Optional[bool] = None
    value: Optional[str] = None
    score: Optional[int] = None
    observation: Optional[str] = None


# Properties to receive via API on creation
class AssessmentCreate(AssessmentBase):
    status: bool
    value: str
    score: int
    observation: str
    record_id: UUID


# Properties to receive via API on update
class AssessmentUpdate(AssessmentBase):
    status: Optional[bool] = None
    value: Optional[str] = None
    score: Optional[int] = None
    observation: Optional[str] = None


class AssessmentInDBBase(AssessmentBase):
    uuid: Optional[UUID]
    equipment_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Assessment(AssessmentInDBBase):
    pass


# Additional properties stored in DB
class AssessmentInDB(AssessmentInDBBase):
    pass
