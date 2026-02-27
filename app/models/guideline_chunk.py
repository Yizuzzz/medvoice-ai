import uuid
from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base

class GuidelineChunk(Base):
    __tablename__ = "guideline_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guideline_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clinical_guidelines.id", ondelete="CASCADE"),
        nullable=False
    )

    section = Column(Text, nullable=True)
    page = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))

    guideline = relationship("ClinicalGuideline")