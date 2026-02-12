import uuid
from sqlalchemy import String, Integer, Text, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ClinicalEncounter(Base):
    __tablename__ = "clinical_encounters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    patient_id: Mapped[str] = mapped_column(String, index=True)
    pattient_age: Mapped[int] = mapped_column(Integer)
    patient_gender: Mapped[str] = mapped_column(String)

    audio_path: Mapped[str] = mapped_column(String)
    transcript: Mapped[str] = mapped_column(Text)
    ai_response: Mapped[str] = mapped_column(Text)

    retrived_chunks: Mapped[dict] = mapped_column(JSON)
    confidence_score: Mapped[float] = mapped_column(Float)

    latency_ms: Mapped[int] = mapped_column(Integer)
    model_used: Mapped[str] = mapped_column(String)
    tokens_used: Mapped[int] = mapped_column(Integer)