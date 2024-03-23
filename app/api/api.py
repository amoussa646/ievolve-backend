from fastapi import APIRouter

from app.api.endpoints import auth, users,activity,dayPlan, habit,today

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(dayPlan.router, prefix="/dayplan", tags=["dayplan"])
api_router.include_router(habit.router, prefix="/habit", tags=["habit"])
api_router.include_router(today.router, prefix="/today", tags=["today"])
