import uuid
from sqlalchemy import Column, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime, timezone

class QueryEvaluation(Base):
    __tablename__ = "query_evaluation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.id", ondelete="CASCADE"))
    relevance_score = Column(Float)
    faithfulness_score = Column(Float)
    notes = Column(Text)
    evaluated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )