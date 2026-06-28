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

import app.core.logging

from app.core.middleware import AuthenticationMiddleware

from app.routes.auth import router as auth_router
from app.routes.farmer import router as farmer_router

from app.routes.farm import router as farm_router


# =====================================================
# FastAPI Application
# =====================================================
app = FastAPI(
    title="VerdiGO AI API",
    description="AI Powered Farmer Companion",
    version="1.0.0"
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


# =====================================================
# Root Endpoint
#
# Used for:
# - Health check
# - API welcome message
# - Quick deployment verification
# =====================================================
@app.get("/")
def root():
    return {
        "message": "Welcome to VerdiGO AI"
    }