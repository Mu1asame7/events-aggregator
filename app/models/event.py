from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    place_id = Column(UUID(as_uuid=True), ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    event_time = Column(DateTime, nullable=False)
    registration_deadline = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    number_of_visitors = Column(Integer, nullable=False)
    changed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    status_changed_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    place = relationship("Place", back_populates="events")

    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")
