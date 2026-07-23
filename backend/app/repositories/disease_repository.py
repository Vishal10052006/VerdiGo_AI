"""
Disease Detection Repository

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.disease_detection import DiseaseDetection


def create(db: Session, detection: DiseaseDetection) -> DiseaseDetection:
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


def get_by_id(db: Session, detection_id: UUID) -> DiseaseDetection | None:
    return (
        db.query(DiseaseDetection)
        .filter(DiseaseDetection.id == detection_id)
        .first()
    )


def get_history_for_farm(
    db: Session,
    farm_id: UUID,
    skip: int = 0,
    limit: int = 20,
) -> list[DiseaseDetection]:
    return (
        db.query(DiseaseDetection)
        .filter(DiseaseDetection.farm_id == farm_id)
        .order_by(DiseaseDetection.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_latest_for_farm(db: Session, farm_id: UUID) -> DiseaseDetection | None:
    return (
        db.query(DiseaseDetection)
        .filter(DiseaseDetection.farm_id == farm_id)
        .order_by(DiseaseDetection.created_at.desc())
        .first()
    )