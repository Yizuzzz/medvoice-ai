from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List

from app.db.session import get_db
from app.services.embeddings import get_embedding
from app.repositories.query_repository import search_similar_queries


router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@router.post("/search")
async def semantic_search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    embedding = get_embedding(request.query)

    results = await search_similar_queries(
        db=db,
        embedding=embedding,
        limit=request.limit
    )

    return [
        {
            "id": str(row.id),
            "question": row.question,
            "response": row.response,
            "distance": float(row.distance),
        }
        for row in results
    ]