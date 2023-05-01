from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class InspectionConditionBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class InspectionConditionCreate(InspectionConditionBase):
    title: str


# Properties to receive via API on update
class InspectionConditionUpdate(InspectionConditionBase):
    title: Optional[str] = None


class InspectionConditionInDBBase(InspectionConditionBase):
    uuid: Optional[UUID]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class InspectionCondition(InspectionConditionInDBBase):
    pass


# Additional properties stored in DB
class InspectionConditionInDB(InspectionConditionInDBBase):
    pass
