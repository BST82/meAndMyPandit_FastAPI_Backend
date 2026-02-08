from fastapi import APIRouter
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from .header_routes import router as header_router
from .footer_routes import router as footer_router
from .home_routes import router as home_router


api_router = APIRouter()

# Attach child routers
api_router.include_router(user_router, prefix="/user", tags=["User Management"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
