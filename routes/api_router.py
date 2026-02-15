from fastapi import APIRouter

from .user_routes import router as user_router
from .auth_routes import router as auth_router
from .header_routes import router as header_router
from .footer_routes import router as footer_router
from .home_routes import router as home_router
from .choghadiya_routes import router as choghadiya_router
from .moonphases_router import router as moonphases_router
from .muhurat_route import router as muhurat_router
from .festival_router import router as festival_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User Management"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(header_router, prefix="/header")
api_router.include_router(footer_router, prefix="/footer")
api_router.include_router(home_router, prefix="/home")
api_router.include_router(choghadiya_router, prefix="/chohadiya")
api_router.include_router(moonphases_router, prefix="/panchang")
api_router.include_router(muhurat_router, prefix="/muhurat")    
api_router.include_router(festival_router, prefix="/festival", tags=["Festival"])