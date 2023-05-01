from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class RiskBase(BaseModel):
    value: Optional[int] = None


# Properties to receive via API on creation
class RiskCreate(RiskBase):
    value: int


# Properties to receive via API on update
class RiskUpdate(RiskBase):
    value: Optional[int] = None


class RiskInDBBase(RiskBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Risk(RiskInDBBase):
    pass


# Additional properties stored in DB
class RiskInDB(RiskInDBBase):
    pass
