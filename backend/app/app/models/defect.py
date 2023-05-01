from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Defect(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    failure = Column(String)
    speciality = Column(String)
    inspection_point = Column(String)
    record_id = Column(UUID(as_uuid=True), ForeignKey('record.uuid'))
