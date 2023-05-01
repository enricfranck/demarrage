from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
from .company import Company

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Site(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    value = Column(String)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.uuid'))

    company = relationship(Company, backref='company')
