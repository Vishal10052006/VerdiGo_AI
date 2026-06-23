from fastapi import FastAPI

app = FastAPI(
    title="VerdiGO AI API",
    description="AI Powered Farmer Companion",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to VerdiGO AI"
    }