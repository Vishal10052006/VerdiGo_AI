"""
Cloudflare R2 Storage Provider

S3-compatible object storage. Survives redeploys, unlike local
disk. Uses boto3's S3 client pointed at R2's S3-compatible endpoint.

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

import boto3
from botocore.client import Config

from app.services.storage.base import ImageStorageProvider
from app.config.settings import settings


class R2StorageProvider(ImageStorageProvider):

    def __init__(self):
        if not all([
            settings.R2_ACCOUNT_ID,
            settings.R2_ACCESS_KEY_ID,
            settings.R2_SECRET_ACCESS_KEY,
            settings.R2_BUCKET_NAME,
        ]):
            raise ValueError("R2 storage credentials are not fully configured.")

        self.bucket = settings.R2_BUCKET_NAME
        self.public_base_url = settings.R2_PUBLIC_BASE_URL.rstrip("/")

        self.client = boto3.client(
            "s3",
            endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )

    def save(self, file_bytes: bytes, filename: str, folder: str) -> str:
        key = f"{folder}/{filename}"

        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file_bytes,
            ContentType=self._guess_content_type(filename),
        )

        return f"{self.public_base_url}/{key}"

    def delete(self, url: str) -> None:
        key = url.replace(f"{self.public_base_url}/", "", 1)
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
        except Exception:
            # Deletion is best-effort — a missing object shouldn't
            # break the caller's flow (e.g. re-upload after failed delete).
            pass

    @staticmethod
    def _guess_content_type(filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        return {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
        }.get(ext, "application/octet-stream")