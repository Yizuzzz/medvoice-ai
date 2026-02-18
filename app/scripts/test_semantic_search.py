import asyncio

from app.services.embeddings import get_embedding
from app.db.session import AsyncSessionLocal
from app.repositories.query_repository import search_similar_queries


async def main():
    async with AsyncSessionLocal() as db:

        query_text = "Diabetes mellitus tipo 2 diagnóstico"

        print("🔎 Generando embedding de búsqueda...")
        embedding = get_embedding(query_text)

        results = await search_similar_queries(
            db=db,
            embedding=embedding,
            limit=5
        )

        print("\n🎯 Resultados encontrados:\n")

        for row in results:
            print(f"ID: {row.id}")
            print(f"Pregunta: {row.question}")
            print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())
