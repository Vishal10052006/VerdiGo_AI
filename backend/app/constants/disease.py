"""
Disease Detection Constants

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

# Image validation — same envelope as profile image upload,
# but disease photos legitimately need to be larger (crop close-ups).
ALLOWED_DISEASE_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
MAX_DISEASE_IMAGE_SIZE = 8 * 1024 * 1024  # 8 MB

# Confidence below this, treat AI result as "inconclusive" rather
# than presenting a false-confidence diagnosis to the farmer.
MIN_CONFIDENCE_THRESHOLD = 35.0

DISEASE_HISTORY_DEFAULT_LIMIT = 20