from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class DefectBase(BaseModel):
    speciality: Optional[str]
    failure: Optional[str]
    inspection_point: Optional[str]


# Properties to receive via API on creation
class DefectCreate(DefectBase):
    speciality: str
    failure: str
    inspection_point: str
    record_id: UUID


# Properties to receive via API on update
class DefectUpdate(DefectBase):
    speciality: Optional[str]
    failure: Optional[str]
    inspection_point: Optional[str]


class DefectInDBBase(DefectBase):
    uuid: Optional[UUID]
    record_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Defect(DefectInDBBase):
    pass


# Additional properties stored in DB
class DefectInDB(DefectInDBBase):
    pass
