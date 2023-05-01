from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class CriticalityBase(BaseModel):
    value: Optional[int] = None


# Properties to receive via API on creation
class CriticalityCreate(CriticalityBase):
    value: int


# Properties to receive via API on update
class CriticalityUpdate(CriticalityBase):
    value: Optional[int] = None


class CriticalityInDBBase(CriticalityBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Criticality(CriticalityInDBBase):
    pass


# Additional properties stored in DB
class CriticalityInDB(CriticalityInDBBase):
    pass
