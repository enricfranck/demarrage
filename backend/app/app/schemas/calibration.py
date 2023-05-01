from datetime import date
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class CalibrationBase(BaseModel):
    value: Optional[bool] = None
    date_status: Optional[date]
    next_date: Optional[date]


# Properties to receive via API on creation
class CalibrationCreate(CalibrationBase):
    value: bool
    date_status: date
    next_date: date


# Properties to receive via API on update
class CalibrationUpdate(CalibrationBase):
    pass


class CalibrationInDBBase(CalibrationBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Calibration(CalibrationInDBBase):
    pass


# Additional properties stored in DB
class CalibrationInDB(CalibrationInDBBase):
    pass
