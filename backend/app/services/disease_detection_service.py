"""
Disease Detection Service

Orchestrates: image validation → storage → Gemini Vision
analysis → persistence. Mirrors the CropRecommendationService
pattern (ownership-scoped, one public entrypoint, persisted run).

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

import os
import uuid

import httpx
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.constants.disease import (
    ALLOWED_DISEASE_IMAGE_EXTENSIONS,
    MAX_DISEASE_IMAGE_SIZE,
    MIN_CONFIDENCE_THRESHOLD,
    DISEASE_HISTORY_DEFAULT_LIMIT,
)
from app.enums.disease_severity import DiseaseSeverityEnum
from app.models.disease_detection import DiseaseDetection
from app.repositories import disease_repository, farm_repository
from app.services.ai.gemini_vision_client import GeminiVisionClient
from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
    ServiceUnavailableException,
)

_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


class DiseaseDetectionService:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------------
    # Detect Disease (public entrypoint)
    # ------------------------------------------------------------------------

    def detect(
        self,
        farm_id: uuid.UUID,
        user_id: uuid.UUID,
        file: UploadFile,
        crop_type: str | None = None,
    ) -> DiseaseDetection:
        """
        Analyze an uploaded crop image and persist the result.

        Ownership-scoped exactly like crop recommendation: a farm
        that exists but belongs to someone else returns the same
        404 as a farm that doesn't exist at all.
        """

        farm = farm_repository.get_by_id_for_user(
            db=self.db, farm_id=farm_id, user_id=user_id
        )
        if farm is None:
            raise NotFoundException(message="Farm not found.")

        # ----------------------------------------------------------------
        # Validate & Read Image
        # ----------------------------------------------------------------

        extension = os.path.splitext(file.filename or "")[1].lower()

        if extension not in ALLOWED_DISEASE_IMAGE_EXTENSIONS:
            raise BadRequestException(
                message=(
                    "Invalid image format. Allowed: "
                    f"{', '.join(ALLOWED_DISEASE_IMAGE_EXTENSIONS)}"
                )
            )

        image_bytes = file.file.read()
        file.file.seek(0)

        if not image_bytes:
            raise BadRequestException(message="Uploaded file is empty.")

        if len(image_bytes) > MAX_DISEASE_IMAGE_SIZE:
            raise BadRequestException(
                message=(
                    f"Image exceeds maximum size of "
                    f"{MAX_DISEASE_IMAGE_SIZE // (1024 * 1024)} MB."
                )
            )

        # ----------------------------------------------------------------
        # AI Vision Analysis (before we commit to storing the file —
        # no point keeping an image whose analysis failed)
        # ----------------------------------------------------------------

        mime_type = _MIME_TYPES[extension]

        try:
            vision_client = GeminiVisionClient()
            ai_output = vision_client.analyze_image(image_bytes, mime_type)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError):
            raise ServiceUnavailableException(
                message="AI Vision service is temporarily unavailable. Please try again shortly."
            )
        except ValueError:
            raise ServiceUnavailableException(
                message="AI Vision could not analyze this image. Please try a clearer photo."
            )

        result = ai_output["result"]

        # ----------------------------------------------------------------
        # Persist Image
        # ----------------------------------------------------------------

        filename = f"{uuid.uuid4()}{extension}"
        file_path = os.path.join(settings.DISEASE_UPLOAD_DIR, filename)

        os.makedirs(settings.DISEASE_UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as image_file:
            image_file.write(image_bytes)

        image_url = f"/uploads/disease/{filename}"

        # ----------------------------------------------------------------
        # Normalize AI Output
        # ----------------------------------------------------------------

        confidence = float(result.get("confidence", 0))
        is_healthy = bool(result.get("is_healthy", False))

        # Low-confidence results are surfaced as inconclusive rather
        # than a confident-sounding wrong diagnosis — this matters a
        # lot more for a farmer's livelihood than a normal chat reply.
        if confidence < MIN_CONFIDENCE_THRESHOLD and not is_healthy:
            severity = DiseaseSeverityEnum.NONE
            disease_name = "Inconclusive — please retake a closer, well-lit photo"
            treatment = ["Retake the photo in good daylight, focused on the affected leaf/area."]
        else:
            severity = DiseaseSeverityEnum(result.get("severity", "none"))
            disease_name = result.get("disease_name") if not is_healthy else None
            treatment = result.get("treatment", []) or []

        detection = DiseaseDetection(
            farm_id=farm_id,
            image_url=image_url,
            crop_type=crop_type or result.get("crop_identified"),
            is_healthy=is_healthy,
            disease_name=disease_name,
            confidence=confidence,
            severity=severity,
            treatment=treatment,
            prevention_tips=result.get("prevention_tips", []) or [],
            ai_provider="gemini",
        )

        return disease_repository.create(db=self.db, detection=detection)

    # ------------------------------------------------------------------------
    # Get History
    # ------------------------------------------------------------------------

    def get_history(
        self,
        farm_id: uuid.UUID,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = DISEASE_HISTORY_DEFAULT_LIMIT,
    ) -> list[DiseaseDetection]:
        farm = farm_repository.get_by_id_for_user(
            db=self.db, farm_id=farm_id, user_id=user_id
        )
        if farm is None:
            raise NotFoundException(message="Farm not found.")

        return disease_repository.get_history_for_farm(
            db=self.db, farm_id=farm_id, skip=skip, limit=limit
        )

    # ------------------------------------------------------------------------
    # Get Single Detection
    # ------------------------------------------------------------------------

    def get_detection(
        self,
        detection_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> DiseaseDetection:
        detection = disease_repository.get_by_id(self.db, detection_id)
        if detection is None:
            raise NotFoundException(message="Detection not found.")

        owned_farm = farm_repository.get_by_id_for_user(
            db=self.db, farm_id=detection.farm_id, user_id=user_id
        )
        if owned_farm is None:
            raise NotFoundException(message="Detection not found.")

        return detection