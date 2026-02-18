import asyncio
import uuid
from datetime import datetime, timezone


from app.services.embeddings import get_embedding
from app.db.session import AsyncSessionLocal
from app.db.models.query import Query

async def main():
    async with AsyncSessionLocal() as db:

        text = "¿Qué determina el diagnostico de un diabetes mellitus tipo 2?"
        print("Generando embedding...")
        embedding = get_embedding(text)

        print(f"Dimensión del embedding: {len(embedding)}")

        new_query = Query(
            id=uuid.uuid4(),
            question=text,
            embedding=embedding,
            created_at=datetime.now(timezone.utc),
        )

        db.add(new_query)
        await db.commit()

        print("Embedding guardado correctamente en la bd")

if __name__ == "__main__":
    asyncio.run(main())