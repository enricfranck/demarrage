from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class AnneUnivBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class AnneUnivCreate(AnneUnivBase):
    title: str


# Properties to receive via API on update
class AnneUnivUpdate(AnneUnivBase):
    title: Optional[str] = None


class AnneUnivInDBBase(AnneUnivBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class AnneUniv(AnneUnivInDBBase):
    code: Optional[str] = None


# Additional properties stored in DB
class AnneUnivInDB(AnneUnivInDBBase):
    pass
