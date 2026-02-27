import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a clinical AI assistant.

CRITICAL RULES:
- Always respond entirely in the requested language.
- Never mix languages.
- Preserve medical accuracy.
- Keep numerical values and units exactly as provided.

Answer strictly based on the provided ADA guideline context.
If the answer is not in the context, say you don't know.
"""



async def generate_answer(
        question: str,
        context_chunks: list[str],
        language: str
        ):
    context = "\n\n--\n\n".join(context_chunks)

    user_prompt = f"""
Context:
{context}

Question:
{question}

Respond only in {language}.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content
