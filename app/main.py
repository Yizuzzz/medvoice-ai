from fastapi import FastAPI
from app.api.routes import clinical_encounters
from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes import search
from app.api.routes.search import router as search_router
from app.api.routes.query import router as query_router
from app.api.routes import ask

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(clinical_encounters.router)
#app.include_router(search_router)
app.include_router(query_router)
app.include_router(search.router)
app.include_router(ask.router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "environment": settings.ENV,
    }

