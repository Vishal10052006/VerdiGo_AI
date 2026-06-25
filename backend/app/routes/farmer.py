from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/farmer",
    tags=["Farmer"]
)


@router.get("/me")
def get_profile(
    current_user=Depends(get_current_user)
):
    return {
        "mobile": current_user["mobile"],
        "message": "Authenticated successfully"
    }