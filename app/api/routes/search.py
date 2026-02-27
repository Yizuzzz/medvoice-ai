from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.repositories.guideline_repository import search_guideline_chunks

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    results = await search_guideline_chunks(
        db=db,
        query=request.query,
        k=request.k
    )
    return {"results": results}