from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.guideline_repository import search_guideline_chunks
from app.services.qa_service import generate_answer
from app.schemas.ask import AskRequest
from app.services.lenguage_service import detect_language

router = APIRouter(prefix="/ask", tags=["ask"])
ALLOWED_LANGUAGES = {"en", "es", "fr", "pt", "de"}
SIMILARITY_THRESHOLD = 0.6

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

    filtered_results = [
        r for r in results
        if r["score"] <= SIMILARITY_THRESHOLD
    ]

    if not filtered_results:
        return {
            "answer": "No relevant guideline content found for this question.",
            "language": detected_language,
            "sources": [],
            "retrieval": {
                "total_chunks": len(results),
                "used_chunks": 0,
                "threshold": SIMILARITY_THRESHOLD
            }
        }
    
    context_chunks = [r["content"] for r in filtered_results]

    response_data = await generate_answer(
        question=user_question,
        context_chunks=context_chunks,
        language=detected_language
    )

    return {
        "answer": response_data["answer"],
        "citations": response_data["citations"],
        "language": detected_language,
        "sources": filtered_results,
        "retrieval": {
            "total_chunks": len(results),
            "used_chunks": len(filtered_results),
            "threshold": SIMILARITY_THRESHOLD
        }
    }
