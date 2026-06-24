from fastapi import FastAPI

from app.routes.auth import router as auth_router

app = FastAPI(
    title="VerdiGO AI API",
    description="AI Powered Farmer Companion",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to VerdiGO AI"
    }