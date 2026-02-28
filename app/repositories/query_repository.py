import time
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.services.ingestion.embedder import get_embedding
import uuid

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

async def save_query(
        db: AsyncSession,
        question: str,
        response: str,
        model_used: str,
):
    start_time = time.time()

    embedding = get_embedding(question)

    latency_ms = int((time.time() - start_time) * 1000)

    await db.execute(
        text("""
            INSERT INTO queries (
                id,
                question,
                embedding,
                response,
                model_used,
                latency_ms,
                created_at
            )
            VALUES (
                :id,
                :question,
                :embeding::vector,
                :response,
                :model_used,
                :latency_ms,
                NOW()
            )
        """),
        {
            "id": str(uuid.uuid4()),
            "question": question,
            "embeding": embedding,
            "response": response,
            "model_used": model_used,
            "latency_ms": latency_ms
        }
    )

    await db.commit()