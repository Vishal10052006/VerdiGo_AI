"""
Profile Constants

Centralized constants for profile image processing.

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Image Resize Configuration
# ============================================================================

# Max dimensions for a profile avatar — square-ish crop target.
# 512x512 is generous for any UI avatar use case (list rows, headers,
# even a large profile-page hero image) while keeping file size small.
PROFILE_IMAGE_MAX_DIMENSION = 512

# JPEG/WebP compression quality (1-95, Pillow's recommended ceiling).
# 85 is the standard "visually lossless to the eye, meaningfully smaller
# file" sweet spot used by most image pipelines (imgix, Cloudinary defaults
# sit in the 80-85 range).
PROFILE_IMAGE_QUALITY = 85

# Output format profile images are normalized to, regardless of upload
# format. Keeps stored files predictable/consistent and avoids storing
# PNGs (much larger for photographic content) when a JPEG works fine.
# Uploads with transparency (PNG) get flattened onto a white background
# before conversion — see _flatten_to_rgb().
PROFILE_IMAGE_OUTPUT_FORMAT = "JPEG"
PROFILE_IMAGE_OUTPUT_EXTENSION = ".jpg"