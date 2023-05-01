from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.dialects.postgresql.base import UUID
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Calibration(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(Boolean(), default=False)
    date_status = Column(Date)
    next_date = Column(Date)
    # equipment = relationship("Equipment", backref="calibration", cascade="all, delete")
