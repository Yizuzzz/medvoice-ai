from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ingestion.embedder import get_embedding


async def search_guideline_chunks(
    db: AsyncSession,
    query: str,
    k: int = 5
):
    query_embedding = get_embedding(query)

    sql = text("""
        SELECT content, guideline_id,
               embedding <=> CAST(:embedding AS vector) AS distance
        FROM guideline_chunks
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :k
    """)

    result = await db.execute(
        sql,
        {
            "embedding": query_embedding,
            "k": k
        }
    )

    rows = result.fetchall()

    return [
        {
            "content": row.content,
            "guideline_id": row.guideline_id,
            "score": float(row.distance)
        }
        for row in rows
    ]
