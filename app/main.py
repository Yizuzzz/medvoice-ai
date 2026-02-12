from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.health import router as health_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0"
)

app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "environment": settings.ENV,
    }

