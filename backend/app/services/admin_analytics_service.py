# backend/app/services/admin_analytics_service.py
"""
Admin Analytics Service

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.repositories import admin_analytics_repository as repo


def get_overview(db: Session) -> dict:
    total_farmers = repo.count_farmers(db)
    active_farmers = repo.count_active_farmers(db)
    total_farms = repo.count_farms(db)
    completed_profiles = repo.count_completed_profiles(db)

    now = datetime.now(timezone.utc)
    new_7d = repo.count_new_farmers_since(db, now - timedelta(days=7))
    new_30d = repo.count_new_farmers_since(db, now - timedelta(days=30))

    completion_rate = (
        round((completed_profiles / total_farmers) * 100, 1) if total_farmers else 0.0
    )

    soil_dist = {
        (soil.value if hasattr(soil, "value") else str(soil)): count
        for soil, count in repo.soil_type_distribution(db)
    }
    state_dist = {state or "Unknown": count for state, count in repo.state_distribution(db)}

    return {
        "total_farmers": total_farmers,
        "active_farmers": active_farmers,
        "total_farms": total_farms,
        "profile_completion_rate": completion_rate,
        "new_farmers_last_7_days": new_7d,
        "new_farmers_last_30_days": new_30d,
        "total_crop_recommendations": repo.count_crop_recommendations(db),
        "total_disease_detections": repo.count_disease_detections(db),
        "total_chat_messages": repo.count_chat_messages(db),
        "soil_type_distribution": soil_dist,
        "state_distribution": state_dist,
    }


def get_growth(db: Session, days: int = 30) -> dict:
    days = min(max(days, 1), 180)
    rows = repo.daily_signups(db, days)

    return {
        "days": days,
        "signups": [{"date": day, "count": count} for day, count in rows],
    }