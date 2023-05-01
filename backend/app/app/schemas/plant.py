from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class PlantBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class PlantCreate(PlantBase):
    title: str


# Properties to receive via API on update
class PlantUpdate(PlantBase):
    title: Optional[str] = None


class PlantInDBBase(PlantBase):
    uuid: Optional[UUID]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class Plant(PlantInDBBase):
    pass


# Additional properties stored in DB
class PlantInDB(PlantInDBBase):
    pass
