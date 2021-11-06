from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class ParcoursBase(BaseModel):
    title: Optional[str] = None
    uuid_mention: Optional[str] = None


# Properties to receive via API on creation
class ParcoursCreate(ParcoursBase):
    title: str
    uuid_mention: str


# Properties to receive via API on update
class ParcoursUpdate(ParcoursBase):
    title: Optional[str] = None
    uuid_mention: Optional[UUID] = None


class ParcoursInDBBase(ParcoursBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Parcours(ParcoursInDBBase):
    pass


# Additional properties stored in DB
class ParcoursInDB(ParcoursInDBBase):
    pass
