import uuid
from sqlalchemy import Column, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.db.base import Base
from datetime import datetime, timezone

class Query(Base):
    __tablename__ = "queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    question = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    response = Column(Text)
    model_used = Column(Text)
    latency_ms = Column(Integer)
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
        )