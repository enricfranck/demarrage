from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel
from datetime import date

# Shared properties
class RecordBase(BaseModel):
    date: Optional[date]
    date_utc: Optional[date]
    week: Optional[int]
    edited: Optional[bool]
    issued_report_date_utc: Optional[date]
    issued_report_date: Optional[date]
    user_id: Optional[UUID]
    analysis: Optional[str]
    recommendation_action: Optional[str]
    review_user_id: Optional[UUID]
    recommended_action_date: Optional[date]
    planning_team: Optional[str]
    safety_environment: Optional[bool] = False
    register_date: Optional[date]
    inspection_type_id: Optional[UUID]
    failure_progress_id: Optional[UUID]
    calibration_id: Optional[UUID]
    inspection_condition_id: Optional[UUID]
    risk_score_id: Optional[UUID]
    initial_risk_id: Optional[UUID]
    status_id: Optional[UUID]
    recommendation_status_id: Optional[UUID]
    equipment_group_id: Optional[UUID]



# Properties to receive via API on creation
class RecordCreate(RecordBase):
    date: date
    date_utc: date
    week: int
    edited: bool
    issued_report_date_utc: date
    issued_report_date: date
    user_id: UUID
    analysis: Optional[str]
    recommendation_action: Optional[str]
    review_user_id: Optional[UUID]
    recommended_action_date: Optional[date]
    planning_team: Optional[str]
    safety_environment: Optional[bool] = False
    register_date: Optional[date]
    inspection_type_id: Optional[UUID]
    failure_progress_id: Optional[UUID]
    calibration_id: Optional[UUID]
    inspection_condition_id: Optional[UUID]
    risk_score_id: Optional[UUID]
    initial_risk_id: Optional[UUID]
    status_id: Optional[UUID]
    recommendation_status_id: Optional[UUID]
    equipment_group_id: Optional[UUID]


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    pass


class RecordInDBBase(RecordBase):
    uuid: Optional[UUID]
    user_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Record(RecordInDBBase):
    pass


# Additional properties stored in DB
class RecordInDB(RecordInDBBase):
    pass
