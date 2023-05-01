from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class EquipmentGroupBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class EquipmentGroupCreate(EquipmentGroupBase):
    title: str


# Properties to receive via API on update
class EquipmentGroupUpdate(EquipmentGroupBase):
    pass


class EquipmentGroupInDBBase(EquipmentGroupBase):
    uuid: Optional[UUID]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class EquipmentGroup(EquipmentGroupInDBBase):
    pass


# Additional properties stored in DB
class EquipmentGroupInDB(EquipmentGroupInDBBase):
    pass
