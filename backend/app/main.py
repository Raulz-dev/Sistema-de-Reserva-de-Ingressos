from fastapi import FastAPI

from app.config.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health", tags=["Health"])
def read_health():
    return {
            "status": "healthy",
            "environment": settings.app_env,
            }