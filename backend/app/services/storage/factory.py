"""
Storage Provider Factory

Single switch point: STORAGE_PROVIDER env var decides local vs R2.
Imports are lazy (inside the branch) so local-only setups never
need boto3 installed, and R2 credentials are only validated when
R2 mode is actually selected.

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

from functools import lru_cache

from app.services.storage.base import ImageStorageProvider
from app.config.settings import settings


@lru_cache
def get_storage_provider() -> ImageStorageProvider:
    if settings.STORAGE_PROVIDER == "r2":
        from app.services.storage.r2_storage import R2StorageProvider
        return R2StorageProvider()

    from app.services.storage.local_storage import LocalStorageProvider
    return LocalStorageProvider()