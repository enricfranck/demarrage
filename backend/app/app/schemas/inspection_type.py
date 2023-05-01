from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class InspectionTypeBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class InspectionTypeCreate(InspectionTypeBase):
    title: str


# Properties to receive via API on update
class InspectionTypeUpdate(InspectionTypeBase):
    title: Optional[str] = None


class InspectionTypeInDBBase(InspectionTypeBase):
    uuid: Optional[UUID]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class InspectionType(InspectionTypeInDBBase):
    pass


# Additional properties stored in DB
class InspectionTypeInDB(InspectionTypeInDBBase):
    pass
