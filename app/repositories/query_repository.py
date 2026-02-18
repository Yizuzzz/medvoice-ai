from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def search_similar_queries(
        db: AsyncSession,
        embedding: List[float],
        limit: int = 5
):

    await db.execute(text("SET ivfflat.probes = 10;"))

    stmt = text("""
        SELECT id, question, response,
                embedding <=> CAST(:embedding AS vector) AS distance
        FROM queries
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = await db.execute(
        stmt,
        {
            "embedding": embedding,
            "limit": limit
        }
    )

    return result.fetchall()