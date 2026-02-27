import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a clinical AI assistant.

CRITICAL RULES:
- Always respond entirely in the requested language.
- Never mix languages.
- Preserve medical accuracy.
- Keep numerical values and units exactly as provided.
- Extract and list recommendation numbers explicitly (e.g., 2.1a, 2.1b).

You MUST respond in valid JSON with the following structure:

{
  "answer": "string",
  "citations": ["string"]
}

If no recommendation number is present in the context, return an empty list.
Answer strictly based on the provided ADA guideline context.
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
Return only valid JSON.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    content =  response.choices[0].message.content

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "answer": content,
            "citations": []
        }
    
    return parsed