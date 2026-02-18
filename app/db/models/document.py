from app.db.base import Base
import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime
from datetime import datetime, timezone

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    source = Column(Text)
    file_path = Column(Text)
    extra_metadata = Column(JSONB)
    status = Column(Text, default="pending")
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    processed_at = Column(DateTime(timezone=True))