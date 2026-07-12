"""
VerdiGO AI Backend

Main FastAPI application.

Responsibilities:
- Create FastAPI application
- Register middleware
- Register API routers
- Expose root endpoint
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config.settings import settings

import app.core.logging

from app.core.middleware import AuthenticationMiddleware

from app.routes.auth import router as auth_router
from app.routes.farmer import router as farmer_router
from app.routes.farm import router as farm_router
from app.routes.profile import router as profile_router
from app.routes.dashboard import router as dashboard_router
from app.routes.weather import router as weather_router


# =====================================================
# FastAPI Application
# =====================================================
app = FastAPI(
    title="VerdiGO AI API",
    description="AI Powered Farmer Companion",
    version="1.0.0",
    contact={
        "name": "VerdiGO Team",
        "email": "verdigoai@gmail.com",
    },
)


# =====================================================
# Register Global Middleware
# =====================================================
app.add_middleware(
    AuthenticationMiddleware
)


# =====================================================
# Register API Routers
# =====================================================
app.include_router(auth_router)
app.include_router(farmer_router)
app.include_router(farm_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(weather_router)
app.include_router(auth_router, prefix="/api/v1")


# =====================================================
# Static Files
#
# Serves uploaded profile images.
# Example:
# http://127.0.0.1:8000/uploads/profile/image.jpg
# =====================================================

app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)


# =====================================================
# Root Endpoint
#
# Used for:
# - Health check
# - API welcome message
# - Quick deployment verification
# =====================================================
@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Welcome to VerdiGO AI"
    }