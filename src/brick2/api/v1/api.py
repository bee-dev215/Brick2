"""API v1 router."""

from fastapi import APIRouter

from .endpoints import users, campaigns, ads, performance

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(ads.router, prefix="/ads", tags=["ads"])
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])
