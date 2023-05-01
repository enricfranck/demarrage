from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Equipment(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identification = Column(String)
    description = Column(String)
    site_id = Column(UUID(as_uuid=True), ForeignKey('site.uuid'))
    plant_id = Column(UUID(as_uuid=True), ForeignKey('plant.uuid'))
    criticality_id = Column(UUID(as_uuid=True), ForeignKey('criticality.uuid'))
    area = Column(String)
    group = Column(String)
    type = Column(String)
