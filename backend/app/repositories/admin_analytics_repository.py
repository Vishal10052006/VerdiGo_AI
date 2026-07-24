# backend/app/repositories/admin_analytics_repository.py
"""
Admin Analytics Repository

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.farmer_profile import FarmerProfile
from app.models.farm import Farm
from app.models.crop_recommendation import CropRecommendation
from app.models.disease_detection import DiseaseDetection
from app.models.chat import ChatMessage


def count_farmers(db: Session) -> int:
    return db.query(func.count(User.id)).filter(User.role == "farmer").scalar() or 0


def count_active_farmers(db: Session) -> int:
    return (
        db.query(func.count(User.id))
        .filter(User.role == "farmer", User.is_active.is_(True))
        .scalar()
        or 0
    )


def count_farms(db: Session) -> int:
    return db.query(func.count(Farm.id)).scalar() or 0


def count_completed_profiles(db: Session) -> int:
    return (
        db.query(func.count(FarmerProfile.id))
        .filter(FarmerProfile.profile_completed.is_(True))
        .scalar()
        or 0
    )


def count_new_farmers_since(db: Session, since: datetime) -> int:
    return (
        db.query(func.count(User.id))
        .filter(User.role == "farmer", User.created_at >= since)
        .scalar()
        or 0
    )


def count_crop_recommendations(db: Session) -> int:
    return db.query(func.count(CropRecommendation.id)).scalar() or 0


def count_disease_detections(db: Session) -> int:
    return db.query(func.count(DiseaseDetection.id)).scalar() or 0


def count_chat_messages(db: Session) -> int:
    return db.query(func.count(ChatMessage.id)).scalar() or 0


def soil_type_distribution(db: Session) -> list[tuple[str, int]]:
    return (
        db.query(Farm.soil_type, func.count(Farm.id))
        .group_by(Farm.soil_type)
        .all()
    )


def state_distribution(db: Session) -> list[tuple[str, int]]:
    return (
        db.query(FarmerProfile.state, func.count(FarmerProfile.id))
        .group_by(FarmerProfile.state)
        .order_by(func.count(FarmerProfile.id).desc())
        .limit(10)
        .all()
    )


def daily_signups(db: Session, days: int) -> list[tuple[str, int]]:
    since = datetime.now(timezone.utc) - timedelta(days=days)

    rows = (
        db.query(
            func.date(User.created_at).label("day"),
            func.count(User.id),
        )
        .filter(User.role == "farmer", User.created_at >= since)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    )

    return [(str(day), count) for day, count in rows]