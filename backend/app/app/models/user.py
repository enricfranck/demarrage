from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.base import UUID
import uuid

from sqlalchemy.sql.sqltypes import ARRAY
from app.db.base_class import Base


class User(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    role_id = Column(ARRAY(UUID))
    team_id = Column(UUID(as_uuid=True), ForeignKey('team.uuid'))

