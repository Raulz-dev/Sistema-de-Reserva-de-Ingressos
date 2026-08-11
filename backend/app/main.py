from fastapi import FastAPI

from app.config.settings import settings
from app.users.presentation.router import router as users_router

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health", tags=["Health"])
def read_health():

    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


app.include_router(users_router)
