from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
from app.schemas import Team


class CategoryBase(BaseModel):
    title: Optional[str] = None
    team_id: Optional[str]


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    title: str
    team_id : UUID


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    title: Optional[str] = None


class CategoryInDBBase(CategoryBase):
    uuid: Optional[UUID]
    team: Optional[Team]
    value: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Category(CategoryInDBBase):
    pass


# Additional properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
