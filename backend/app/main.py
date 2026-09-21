from fastapi import APIRouter, FastAPI

from app.cinemas.presentation.router import router as cinemas_router
from app.config.settings import settings
from app.movies.presentation.router import router as movies_router
from app.sessions.presentation.router import router as sessions_router
from app.users.presentation.auth_router import router as auth_router
from app.users.presentation.router import router as users_router

app = FastAPI(title=settings.app_name, debug=settings.debug)
api_v1 = APIRouter(prefix="/api/v1")


@app.get("/health", tags=["Health"])
def read_health():

    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


api_v1.include_router(users_router)
api_v1.include_router(auth_router)
api_v1.include_router(movies_router)
api_v1.include_router(cinemas_router)
api_v1.include_router(sessions_router)


app.include_router(api_v1)
