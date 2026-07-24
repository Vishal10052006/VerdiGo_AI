"""
Local Disk Storage Provider

Current default. Fine for local dev; NOT durable on
Railway/Render (ephemeral filesystem wipes on redeploy).

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

import os

from app.services.storage.base import ImageStorageProvider
from app.config.settings import settings


class LocalStorageProvider(ImageStorageProvider):

    def save(self, file_bytes: bytes, filename: str, folder: str) -> str:
        directory = os.path.join(settings.UPLOAD_DIR, folder)
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        return f"/uploads/{folder}/{filename}"

    def delete(self, url: str) -> None:
        relative = url.replace("/uploads/", "", 1)
        file_path = os.path.join(settings.UPLOAD_DIR, relative)

        if os.path.exists(file_path):
            os.remove(file_path)