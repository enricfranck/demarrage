from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class CompanyBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class CompanyCreate(CompanyBase):
    name: str


# Properties to receive via API on update
class CompanyUpdate(CompanyBase):
    name: Optional[str] = None


class CompanyInDBBase(CompanyBase):
    uuid: Optional[UUID]
    value: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Company(CompanyInDBBase):
    pass


# Additional properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass
