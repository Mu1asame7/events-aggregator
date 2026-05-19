from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base


class SyncMetadata(Base):
    __tablename__ = "syncmetadata"

    id = Column(Integer, primary_key=True)
    last_sync_started_at = Column(DateTime, nullable=True)
    last_sync_completed_at = Column(DateTime, nullable=True)
    last_changed_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
