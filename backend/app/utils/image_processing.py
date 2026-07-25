"""
Image Processing Utilities

Shared image resize/compression logic. Currently used by profile
image upload; disease detection intentionally does NOT resize
(diagnostic accuracy depends on original resolution/detail), so
this stays a profile-specific utility rather than a generic one
applied everywhere.

Module:
Shared Utility

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import io

from PIL import Image, ImageOps

from app.constants.profile import (
    PROFILE_IMAGE_MAX_DIMENSION,
    PROFILE_IMAGE_QUALITY,
    PROFILE_IMAGE_OUTPUT_FORMAT,
)


# ============================================================================
# Resize + Compress Profile Image
# ============================================================================

def resize_and_compress_profile_image(file_bytes: bytes) -> bytes:
    """
    Downscale and compress an uploaded image for use as a profile avatar.

    Steps:
    1. Open via Pillow (validates it's actually a decodable image —
       an extra layer of defense beyond the extension check, which
       only looks at the filename string and can be spoofed).
    2. Apply EXIF orientation correction (phone camera uploads are
       very often stored sideways/upside-down with orientation only
       in EXIF metadata; skipping this is a common "why is my avatar
       rotated" bug).
    3. Flatten transparency (PNG/WebP with alpha) onto a white
       background — required before JPEG encoding, which has no
       alpha channel.
    4. Resize so neither dimension exceeds PROFILE_IMAGE_MAX_DIMENSION,
       preserving aspect ratio, only ever downscaling (never upscales
       a smaller image — thumbnail() already guarantees this).
    5. Re-encode as JPEG at PROFILE_IMAGE_QUALITY.

    Raises:
        ValueError: if the bytes cannot be decoded as an image at all
            (corrupt upload, or a non-image file with a spoofed
            image extension).
    """

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.load()  # force full decode now, not lazily later
    except Exception as exc:
        raise ValueError("Uploaded file is not a valid image.") from exc

    image = ImageOps.exif_transpose(image)

    image = _flatten_to_rgb(image)

    image.thumbnail(
        (PROFILE_IMAGE_MAX_DIMENSION, PROFILE_IMAGE_MAX_DIMENSION),
        Image.LANCZOS,
    )

    output = io.BytesIO()

    image.save(
        output,
        format=PROFILE_IMAGE_OUTPUT_FORMAT,
        quality=PROFILE_IMAGE_QUALITY,
        optimize=True,
    )

    return output.getvalue()


# ============================================================================
# Flatten Transparency
# ============================================================================

def _flatten_to_rgb(image: Image.Image) -> Image.Image:
    """
    Convert any mode (RGBA, P with transparency, LA, etc.) to plain RGB,
    compositing transparent areas onto a white background. JPEG output
    has no alpha channel, so this must happen before saving.
    """

    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        background = Image.new("RGB", image.size, (255, 255, 255))
        rgba_image = image.convert("RGBA")
        background.paste(rgba_image, mask=rgba_image.split()[-1])
        return background

    if image.mode != "RGB":
        return image.convert("RGB")

    return image