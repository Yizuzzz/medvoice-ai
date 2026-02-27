from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_db
from app.services.rag_service import ask_question

router = APIRouter()

class AskRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_endpoint(
    payload: AskRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await ask_question(
        question=payload.question,
        db=db
    )
    return result
