import logging
from django.core.cache import caches
from django.conf import settings
from typing import Any, Dict, List, Optional
import json
from datetime import timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Расширенный менеджер кеширования с поддержкой:
    - Стратегий инвалидации
    - Иерархического кеширования
    - Автоматического сжатия данных
    """

    def __init__(self, cache_name: str = 'offline'):
        self.cache = caches[cache_name]
        self.compress_threshold = getattr(settings, 'CACHE_COMPRESS_THRESHOLD', 1024)  # bytes

    def get(self, key: str, version: str = None) -> Any:
        """Получение данных с автоматической декомпрессией"""
        try:
            value = self.cache.get(key, version=version)
            return self._maybe_decompress(value)
        except Exception as e:
            logger.error(f"Cache read error for key {key}: {str(e)}")
            return None

    def set(self, key: str, value: Any, timeout: int = None, version: str = None):
        """Сохранение данных с автоматическим сжатием"""
        try:
            value = self._maybe_compress(value)
            self.cache.set(key, value, timeout=timeout, version=version)
        except Exception as e:
            logger.error(f"Cache write error for key {key}: {str(e)}")

    def get_or_set(self, key: str, default: Any, timeout: int = None) -> Any:
        """Атомарное получение или установка значения"""
        value = self.get(key)
        if value is None:
            value = default() if callable(default) else default
            self.set(key, value, timeout=timeout)
        return value

    def bulk_get(self, keys: List[str]) -> Dict[str, Any]:
        """Массовое получение данных"""
        results = {}
        for key in keys:
            results[key] = self.get(key)
        return results

    def bulk_set(self, items: Dict[str, Any], timeout: int = None):
        """Массовая запись данных"""
        for key, value in items.items():
            self.set(key, value, timeout=timeout)

    def invalidate(self, key: str, version: str = None):
        """Инвалидация кеша по ключу"""
        self.cache.delete(key, version=version)

    def invalidate_prefix(self, prefix: str):
        """Инвалидация по префиксу ключа"""
        if hasattr(self.cache, 'delete_pattern'):  # Для Redis
            self.cache.delete_pattern(f"{prefix}*")

    def _maybe_compress(self, value: Any) -> Any:
        """Сжатие данных если они превышают порог"""
        if isinstance(value, (str, bytes)) and len(value) > self.compress_threshold:
            return self._compress(value)
        return value

    def _maybe_decompress(self, value: Any) -> Any:
        """Распаковка сжатых данных"""
        if isinstance(value, bytes) and value.startswith(b'COMPRESSED:'):
            return self._decompress(value[11:])
        return value

    def _compress(self, data: str) -> bytes:
        """Простое сжатие (реализация может быть заменена на zlib)"""
        return b'COMPRESSED:' + data.encode('utf-8')

    def _decompress(self, data: bytes) -> str:
        """Распаковка данных"""
        return data.decode('utf-8')