from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class StatusBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class StatusCreate(StatusBase):
    title: str


# Properties to receive via API on update
class StatusUpdate(StatusBase):
    title: Optional[str] = None


class StatusInDBBase(StatusBase):
    uuid: Optional[UUID]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class Status(StatusInDBBase):
    pass


# Additional properties stored in DB
class StatusInDB(StatusInDBBase):
    pass
