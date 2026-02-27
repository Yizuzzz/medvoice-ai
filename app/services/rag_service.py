from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.query_repository import search_similar_queries
from app.services.embeddings import get_embedding
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def ask_question(
    question: str,
    db: AsyncSession,
    k: int = 3
):
    # 1️⃣ Generar embedding
    embedding = get_embedding(question)

    # 2️⃣ Buscar similares
    results = await search_similar_queries(
        db=db,
        embedding=embedding,
        limit=k
    )

    # 3️⃣ Construir contexto
    context_blocks = []
    for row in results:
        context_blocks.append(
            f"Pregunta: {row.question}\nRespuesta: {row.response}"
        )

    context = "\n\n".join(context_blocks)

    # 4️⃣ Prompt
    prompt = f"""
Eres un asistente médico profesional.

Responde usando exclusivamente la información del contexto.
únicamente responde a la pregunta si la respuesta se encuentra en el contexto.
No hagas suposiciones ni inventes información.
La única información relevante que puedes responder es sobre medicina, cualquier otro tema lo desconcoes.
Si no encuentras la respuesta en el contexto, di que no tienes suficiente información.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""

    # 5️⃣ Llamar LLM
    completion = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente médico basado en evidencia."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )

    answer = completion.choices[0].message.content

    return {
        "answer": answer,
        "sources": [
            {
                "id": str(row.id),
                "question": row.question,
                "distance": float(row.distance),
            }
            for row in results
        ],
    }
