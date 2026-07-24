# backend/app/enums/notification.py
"""
Notification Type & Severity Enums

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

from enum import Enum


class NotificationTypeEnum(str, Enum):
    WEATHER = "weather"
    DISEASE = "disease"
    CROP = "crop"
    SYSTEM = "system"
    GENERAL = "general"


class NotificationSeverityEnum(str, Enum):
    INFO = "info"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"