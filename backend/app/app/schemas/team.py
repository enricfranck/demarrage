from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
from .site import Site


class TeamBase(BaseModel):
    name: Optional[str] = None
    site_id: Optional[str]


# Properties to receive via API on creation
class TeamCreate(TeamBase):
    name: str
    site_id: str


# Properties to receive via API on update
class TeamUpdate(TeamBase):
    pass


class TeamInDBBase(TeamBase):
    uuid: Optional[UUID]
    value: str
    site: Optional[Site]
    class Config:
        orm_mode = True


# Additional properties to return via API
class Team(TeamInDBBase):
    pass


# Additional properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
