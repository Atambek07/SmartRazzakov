import json
from typing import Dict, List
from django.core.cache import caches
from .cache_manager import CacheManager


class OfflineTaskQueue:
    """
    Очередь задач для выполнения при восстановлении соединения:
    - Логирование действий
    - Отправка отзывов
    - Синхронизация пользовательских данных
    """

    def __init__(self):
        self.cache = CacheManager()
        self.queue_key = "offline_task_queue"

    def add_task(self, task_type: str, data: Dict):
        """Добавление задачи в очередь"""
        queue = self._get_queue()
        queue.append({
            'type': task_type,
            'data': data,
            'attempts': 0
        })
        self._save_queue(queue)

    def process_queue(self):
        """Выполнение задач при появлении соединения"""
        queue = self._get_queue()
        success_tasks = []

        for task in queue:
            try:
                if self._execute_task(task):
                    success_tasks.append(task)
            except Exception:
                task['attempts'] += 1

        # Удаление успешных задач
        self._save_queue([t for t in queue if t not in success_tasks])

    def _execute_task(self, task: Dict) -> bool:
        """Выполнение конкретной задачи"""
        # Реализация для разных типов задач
        return True

    def _get_queue(self) -> List[Dict]:
        """Получение текущей очереди"""
        return json.loads(self.cache.get(self.queue_key) or '[]')

    def _save_queue(self, queue: List[Dict]):
        """Сохранение очереди"""
        self.cache.set(self.queue_key, json.dumps(queue))