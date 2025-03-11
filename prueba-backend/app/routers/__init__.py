from fastapi import APIRouter
from .user_routes import router as user_router
from .history_routes import router as history_router

router = APIRouter()
router.include_router(user_router, prefix="/user")
router.include_router(history_router, prefix="/history")