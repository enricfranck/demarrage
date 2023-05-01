from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class FailureProgressBase(BaseModel):
    title: Optional[str] = None
    value: Optional[int] = None


# Properties to receive via API on creation
class FailureProgressCreate(FailureProgressBase):
    title: str
    value: int


# Properties to receive via API on update
class FailureProgressUpdate(FailureProgressBase):
    title: Optional[str] = None
    value: Optional[int] = None


class FailureProgressInDBBase(FailureProgressBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class FailureProgress(FailureProgressInDBBase):
    pass


# Additional properties stored in DB
class FailureProgressInDB(FailureProgressInDBBase):
    pass
