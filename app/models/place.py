from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    seats_pattern = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    events = relationship(
        "Event", back_populates="place", cascade="all, delete-orphan"
    )
