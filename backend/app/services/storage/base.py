"""
Image Storage Provider Interface

Abstracts WHERE files are stored so services never talk to
disk or S3 directly. Swapping local disk -> R2 is a config
change, not a rewrite.

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

from abc import ABC, abstractmethod


class ImageStorageProvider(ABC):
    """
    Contract every storage backend must implement.
    """

    @abstractmethod
    def save(self, file_bytes: bytes, filename: str, folder: str) -> str:
        """
        Persist file bytes and return a publicly accessible URL.

        Args:
            file_bytes: Raw file content.
            filename: Unique filename (caller generates via uuid4()).
            folder: Logical subfolder, e.g. "disease", "profile".

        Returns:
            Public URL (absolute for R2, relative /uploads/... for local).
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, url: str) -> None:
        """
        Delete a previously stored file by its returned URL.
        Must not raise if the file is already gone.
        """
        raise NotImplementedError