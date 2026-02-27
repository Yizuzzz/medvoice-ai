import uuid
import asyncio

from app.db.session import AsyncSessionLocal
from app.models.clinical_guideline import ClinicalGuideline
from app.models.guideline_chunk import GuidelineChunk

from .pdf_loader import extract_text_from_pdf
from .text_chunker import chunk_text
from .embedder import get_embedding


async def ingest_ada_2025(pdf_path: str):
    print("🚀 Starting ADA ingestion...")

    async with AsyncSessionLocal() as db:

        guideline = ClinicalGuideline(
            id=uuid.uuid4(),
            title="ADA Standards of Care",
            organization="American Diabetes Association",
            year=2025,
            version="2025",
            source_url="https://diabetesjournals-org.translate.goog/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc"
        )

        db.add(guideline)
        await db.flush()

        print("📄 Extracting text...")
        text = extract_text_from_pdf(pdf_path)

        print(f"Text length: {len(text)}")

        chunks = chunk_text(text)

        print(f"Generated {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            print(f"Embedding chunk {i+1}/{len(chunks)}")

            embedding = get_embedding(chunk)

            db_chunk = GuidelineChunk(
                id=uuid.uuid4(),
                guideline_id=guideline.id,
                content=chunk,
                embedding=embedding
            )

            db.add(db_chunk)

        await db.commit()

    print("✅ ADA ingestion completed")
