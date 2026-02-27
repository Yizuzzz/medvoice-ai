from pydantic import BaseModel
from typing import List
from uuid import UUID


class SearchRequest(BaseModel):
    query: str
    k: int = 5


class SearchResult(BaseModel):
    content: str
    guideline_id: UUID
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
