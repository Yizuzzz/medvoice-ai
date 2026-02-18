from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.clinical_encounter_repository import ClinicalEncounterRepository

class ClinicalEncounterService:

    @staticmethod
    async def get_encounters(db):
        return await ClinicalEncounterRepository.get_all(db)
    
    @staticmethod
    async def create_encounter(
        db: AsyncSession,
        patient_id: int,
        transcript: str
    ):
        
        return await ClinicalEncounterRepository.create(
            db,
            patient_id,
            transcript
        )