from fastapi import FastAPI

from app.routes import otp
from app.routes.auth import router as auth_router
from app.routes.login import router as login_router
from app.routes.farmer import router as farmer_router

from fastapi.security import HTTPBearer

app = FastAPI(
    title="VerdiGO AI API",
    description="AI Powered Farmer Companion",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(otp.router)
app.include_router(login_router)
app.include_router(farmer_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to VerdiGO AI"
    }