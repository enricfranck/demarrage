from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
from . import Team

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Category(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    value = Column(String)
    team_id = Column(UUID(as_uuid=True), ForeignKey('team.uuid'))

    team = relationship(Team, backref='team')
