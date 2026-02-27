from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.guideline_repository import search_guideline_chunks
from app.services.qa_service import generate_answer
from app.schemas.ask import AskRequest
from app.services.lenguage_service import detect_language

router = APIRouter(prefix="/ask", tags=["ask"])
ALLOWED_LANGUAGES = {"en", "es", "fr", "pt", "de"}

@router.post("/")
async def ask(
    request: AskRequest,
    db: AsyncSession = Depends(get_db)
):
    user_question = request.question

    detected_language = detect_language(user_question)

    if detected_language not in ALLOWED_LANGUAGES:
        detected_language = "en"

    results = await search_guideline_chunks(
        db=db,
        query=user_question,
        k=5
    )

    context_chunks = [r["content"] for r in results]

    answer = await generate_answer(
        question=user_question,
        context_chunks=context_chunks,
        language=detected_language
    )

    return {
        "answer": answer,
        "sources": results,
        "language": detected_language
    }
