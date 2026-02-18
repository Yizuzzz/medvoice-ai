from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.clinical_encounter import (
    ClinicalEncounterCreate,
    ClinicalEncounterRead
)
from app.services.clinical_encounter_service import ClinicalEncounterService

router = APIRouter(prefix="/encounters", tags=["encounters"])

@router.post("/", response_model=ClinicalEncounterRead)
async def create_encounter(
    payload: ClinicalEncounterCreate,
    db: AsyncSession = Depends(get_db)
):
    return await ClinicalEncounterService.create_encounter(
        db,
        payload.patient_id,
        payload.transcript
    )

@router.get("/")
async def get_encounters(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    return await ClinicalEncounterService.get_encounters(db, limit=limit, offset=offset)