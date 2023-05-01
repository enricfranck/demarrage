from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel
from datetime import date

# Shared properties
from app.schemas import Site, Plant, Criticality


class EquipmentBase(BaseModel):
    identification: Optional[str]
    description: Optional[str]
    site_id: Optional[UUID]
    plant_id: Optional[UUID]
    criticality_id: Optional[UUID]
    area: Optional[str]
    group: Optional[str]
    type: Optional[str]


# Properties to receive via API on creation
class EquipmentCreate(EquipmentBase):
    identification: str
    description: str
    site_id: UUID
    plant_id: UUID
    criticality_id: UUID
    area: str
    group: str
    type: str


# Properties to receive via API on update
class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentInDBBase(EquipmentBase):
    uuid: Optional[UUID]
    site: Optional[Site]
    plant: Optional[Plant]
    criticality: Optional[Criticality]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Equipment(EquipmentInDBBase):
    pass


# Additional properties stored in DB
class EquipmentInDB(EquipmentInDBBase):
    pass
