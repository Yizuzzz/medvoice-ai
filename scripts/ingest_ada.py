print("🔥 SCRIPT STARTED")

import asyncio
from app.services.ingestion.ada_ingest import ingest_ada_2025

if __name__ == "__main__":
    print("🔥 INSIDE MAIN")
    asyncio.run(
        ingest_ada_2025("app/data/ada_2025.pdf")
    )
