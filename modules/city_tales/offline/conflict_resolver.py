from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConflictResolver:
    """
    Механизм разрешения конфликтов при синхронизации:
    - По временным меткам
    - По версиям
    - Ручное разрешение
    """

    def resolve(self, local_data: Dict, remote_data: Dict) -> Dict:
        """
        Автоматическое разрешение конфликта
        :return: Данные для сохранения
        """
        # Стратегия "последнее изменение побеждает"
        local_time = datetime.fromisoformat(local_data['updated_at'])
        remote_time = datetime.fromisoformat(remote_data['updated_at'])

        if remote_time > local_time:
            logger.info("Using remote version as newer")
            return remote_data
        else:
            logger.info("Keeping local version")
            return local_data

    def manual_resolve(self, local: Dict, remote: Dict, strategy: str) -> Dict:
        """Ручное разрешение конфликта"""
        strategies = {
            'remote': lambda: remote,
            'local': lambda: local,
            'merge': self._merge_versions
        }

        if strategy not in strategies:
            raise ValueError(f"Unknown strategy: {strategy}")

        return strategies[strategy](local, remote)

    def _merge_versions(self, local: Dict, remote: Dict) -> Dict:
        """Слияние версий"""
        # Сложная логика слияния
        return {**remote, 'custom_fields': local.get('custom_fields', {})}