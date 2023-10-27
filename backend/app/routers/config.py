from fastapi import APIRouter, Depends
from functools import lru_cache

from app.api.config import Settings

router: APIRouter = APIRouter()
#New decorator for cache
@lru_cache()
def get_settings():
    return Settings()

#Route is used for import settings
@router.get("/api/settings")
async def settings(
    settings: Settings = Depends(get_settings)
) :
    return {
        "SECRET_KEY": settings.SECRET_KEY,
        "APP_MAX": settings.APP_MAX
    }
