from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.clinical_encounter import ClinicalEncounter

class ClinicalEncounterRepository:
    @staticmethod
    async def get_all(db, limit: int = 50, offset: int = 0):
        result = await db.execute(
            select(ClinicalEncounter)
            .limit(limit)
            .offset(offset)
            .order_by(ClinicalEncounter.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def create(
        db: AsyncSession,
        patient_id: int,
        transcript: str
    ) -> ClinicalEncounter:
        
        encounter = ClinicalEncounter(
            patient_id=patient_id,
            transcript=transcript
        )

        db.add(encounter)
        await db.commit()
        await db.refresh(encounter)

        return encounter