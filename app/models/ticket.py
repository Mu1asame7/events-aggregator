from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    seat = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    event = relationship("Event", back_populates="tickets")
