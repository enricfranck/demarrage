from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
from . import RecommendationStatus, EquipmentGroup

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category  # noqa: F401
    from .inspection_type import InspectionType  # noqa: F401
    from .inspection_condition import InspectionCondition  # noqa: F401
    from .risk import Risk  # noqa: F401
    from .status import Status  # noqa: F401
    from .recommendation_status import RecommendationStatus  # noqa: F401
    from .equipment_group import EquipmentGroup  # noqa: F401



class Record(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, default=False)
    date_utc = Column(Date)
    week = Column(Integer)
    edited = Column(Boolean(), default=False)
    issued_report_date = Column(Date)
    issued_report_date_utc = Column(Date)
    analysis = Column(String)
    recommendation_action = Column(String)
    review_user_id = Column(UUID(as_uuid=True), ForeignKey('user.uuid'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.uuid'))
    recommended_action_date = Column(Date)
    planning_team = Column(String)
    safety_environment = Column(Boolean())
    register_date = Column(Date)
    inspection_type_id = Column(UUID(as_uuid=True), ForeignKey('inspection_type.uuid'))
    failure_progress_id = Column(UUID(as_uuid=True), ForeignKey('failure_progress.uuid'))
    calibration_id = Column(UUID(as_uuid=True), ForeignKey('calibration.uuid'))
    risk_score_id = Column(UUID(as_uuid=True), ForeignKey('risk.uuid'))
    initial_risk_id = Column(UUID(as_uuid=True), ForeignKey('risk.uuid'))
    status_id = Column(UUID(as_uuid=True), ForeignKey('status.uuid'))
    recommendation_status_id = Column(UUID(as_uuid=True), ForeignKey('recommendation_status.uuid'))
    equipment_group_id = Column(UUID(as_uuid=True), ForeignKey('equipment_group.uuid'))
    equipment_id = Column(UUID(as_uuid=True), ForeignKey('equipment.uuid'))
    inspection_condition_id = Column(UUID(as_uuid=True), ForeignKey('inspection_condition.uuid'))

