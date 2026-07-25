"""
VerdiGO AI Backend

Main FastAPI application.

Responsibilities:
- Create FastAPI application
- Register middleware
- Register API routers
- Expose root endpoint
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config.settings import settings

import app.core.logging

from app.routes.auth import router as auth_router
from app.routes.farmer import router as farmer_router
from app.routes.farm import router as farm_router
from app.routes.profile import router as profile_router
from app.routes.dashboard import router as dashboard_router
from app.routes.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware

from app.routes.crop_recommendation import router as crop_recommendation_router
from app.routes.chat import router as chat_router
from app.routes.disease import router as disease_router
from app.routes.notification import router as notification_router

from app.routes.admin_auth import router as admin_auth_router
from app.routes.admin_farmer import router as admin_farmer_router
from app.routes.admin_analytics import router as admin_analytics_router


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

# ============================================================================
# CORS
#
# FIX: previously `origins` was a hardcoded literal list containing only
# "http://localhost:3000" — settings.ALLOWED_ORIGINS existed in
# config/settings.py and was fully configured via .env, but was never
# actually read anywhere. This meant ALLOWED_ORIGINS was dead
# configuration: changing it in .env (or in production env vars) had
# ZERO effect, and any deployed frontend not running on localhost:3000
# would be silently CORS-blocked regardless of what you set in prod.
#
# ALLOWED_ORIGINS is a comma-separated string in settings (matching
# .env.test: "ALLOWED_ORIGINS=http://localhost:3000") — parsed here into
# a list. Whitespace around each origin is stripped so
# "a.com, b.com" and "a.com,b.com" both work.
# ============================================================================

origins = [
    origin.strip()
    for origin in settings.ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(crop_recommendation_router)
app.include_router(chat_router)
app.include_router(disease_router)
app.include_router(notification_router)

app.include_router(admin_auth_router)
app.include_router(admin_farmer_router)
app.include_router(admin_analytics_router)

# =====================================================
# Static Files
#
# Serves uploaded profile images.
# Example:
# http://127.0.0.1:8000/uploads/profile/image.jpg
# =====================================================

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "profile"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "disease"), exist_ok=True)

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