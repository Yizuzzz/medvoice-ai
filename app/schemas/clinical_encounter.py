from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ClinicalEncounterCreate(BaseModel):
    patient_id: str
    transcript: str

class ClinicalEncounterRead(BaseModel):
    id: UUID
    patient_id: str
    transcript: str
    created_at: datetime

    class Config:
        from_attributes = True