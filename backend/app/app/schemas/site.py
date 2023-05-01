from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
from .company import Company


class SiteBase(BaseModel):
    name: Optional[str] = None
    company_id: Optional[str]


# Properties to receive via API on creation
class SiteCreate(SiteBase):
    name: str
    company_id: str


# Properties to receive via API on update
class SiteUpdate(SiteBase):
    name: Optional[str] = None
    company_id: Optional[str]


class SiteInDBBase(SiteBase):
    uuid: Optional[UUID]
    company: Optional[Company]
    value: str
    class Config:
        orm_mode = True


# Additional properties to return via API
class Site(SiteInDBBase):
    pass


# Additional properties stored in DB
class SiteInDB(SiteInDBBase):
    pass
