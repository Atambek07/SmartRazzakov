import logging
from typing import List, Dict, Optional
from django.db import transaction
from django.core.cache import caches
from django.conf import settings
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class DataSynchronizer:
    """
    Сервис синхронизации локальных и серверных данных
    Поддерживает:
    - Двустороннюю синхронизацию
    - Разрешение конфликтов
    - Пакетную обработку
    """

    def __init__(self):
        self.cache = caches['offline']
        self.api_base_url = settings.OFFLINE_API_BASE_URL
        self.last_sync_time = self._get_last_sync_time()

    def sync_tales(self, tale_ids: List[str]) -> Dict:
        """
        Синхронизация историй по IDs
        :return: {
            'downloaded': int,
            'uploaded': int,
            'conflicts': int
        }
        """
        try:
            # 1. Получение серверных изменений
            server_data = self._fetch_server_changes(tale_ids)

            # 2. Получение локальных изменений
            local_changes = self._get_local_changes(tale_ids)

            # 3. Разрешение конфликтов и применение изменений
            result = self._apply_changes(server_data, local_changes)

            # 4. Обновление времени синхронизации
            self._update_sync_time()

            return result

        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            raise

    def _fetch_server_changes(self, tale_ids: List[str]) -> Dict:
        """Получение изменений с сервера"""
        try:
            response = requests.post(
                f"{self.api_base_url}/sync/tales",
                json={
                    'ids': tale_ids,
                    'since': self.last_sync_time
                },
                headers={'Authorization': f"Bearer {settings.API_KEY}"}
            )
            response.raise_for_status()
            return response.json().get('data', {})
        except requests.RequestException as e:
            logger.warning(f"Server sync error: {str(e)}")
            return {}

    def _get_local_changes(self, tale_ids: List[str]) -> Dict:
        """Получение локальных изменений из кеша"""
        changes = {}
        for tale_id in tale_ids:
            if cached := self.cache.get(f"tale_{tale_id}_changes"):
                changes[tale_id] = cached
        return changes

    def _apply_changes(self, server_data: Dict, local_changes: Dict) -> Dict:
        """Применение изменений с разрешением конфликтов"""
        result = {'downloaded': 0, 'uploaded': 0, 'conflicts': 0}

        with transaction.atomic():
            # Применение серверных изменений
            for tale_id, data in server_data.items():
                if self._is_newer(data['updated_at']):
                    self._save_tale_locally(data)
                    result['downloaded'] += 1

            # Отправка локальных изменений
            for tale_id, data in local_changes.items():
                if tale_id not in server_data or self._is_newer(data['updated_at']):
                    if self._upload_to_server(data):
                        result['uploaded'] += 1
                        self.cache.delete(f"tale_{tale_id}_changes")
                else:
                    result['conflicts'] += 1
                    self._handle_conflict(tale_id, data, server_data.get(tale_id))

        return result

    def _is_newer(self, timestamp: str) -> bool:
        """Проверка, является ли версия новее последней синхронизации"""
        if not self.last_sync_time:
            return True
        return datetime.fromisoformat(timestamp) > self.last_sync_time

    def _update_sync_time(self):
        """Обновление времени последней синхронизации"""
        self.last_sync_time = datetime.now()
        self.cache.set('last_sync_time', self.last_sync_time.isoformat())

    def _get_last_sync_time(self) -> Optional[datetime]:
        """Получение времени последней синхронизации"""
        if cached := self.cache.get('last_sync_time'):
            return datetime.fromisoformat(cached)
        return None