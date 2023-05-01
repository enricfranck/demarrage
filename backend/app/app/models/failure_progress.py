from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class FailureProgress(Base):
    __tablename__="failure_progress"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    value = Column(Integer)