from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage
from typing import Union, Optional
import mimetypes

class MediaStorage:
    """Унифицированное хранилище для медиа (S3 или локальное)."""

    def __init__(self, use_s3: bool = True):
        self.storage = S3Boto3Storage() if use_s3 else default_storage

    def upload_audio(self, file_data: bytes, filename: str) -> str:
        """Загружает аудиофайл и возвращает URL."""
        content_type = mimetypes.guess_type(filename)[0] or "audio/mpeg"
        path = f"audio/{filename}"
        self.storage.save(path, file_data, content_type=content_type)
        return self.storage.url(path)

    def upload_image(self, file_data: bytes, filename: str) -> str:
        """Загружает изображение и возвращает URL."""
        path = f"images/{filename}"
        self.storage.save(path, file_data)
        return self.storage.url(path)

    def delete_media(self, url: str) -> bool:
        """Удаляет медиафайл по URL."""
        path = self._extract_path(url)
        if path:
            self.storage.delete(path)
            return True
        return False

    def _extract_path(self, url: str) -> Optional[str]:
        """Извлекает путь из URL хранилища."""
        return url.split("/")[-1] if url else None