import zipfile
from io import BytesIO
import json
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class OfflinePackageGenerator:
    """Генератор ZIP-пакетов для офлайн-использования"""
    
    def __init__(self):
        self.base_dir = getattr(settings, 'OFFLINE_STORAGE', 'offline_packages')
        self.max_size_mb = 50  # Максимальный размер пакета

    def generate_package(self, tale_ids: list, user_id: str) -> str:
        """
        Создает ZIP-архив с:
        - JSON-метаданными
        - Аудиофайлами
        - Изображениями
        - HTML-читалкой
        """
        buffer = BytesIO()
        package_name = f"tales_package_{user_id}.zip"
        
        try:
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Добавляем метаданные
                metadata = self._prepare_metadata(tale_ids)
                zipf.writestr('metadata.json', json.dumps(metadata))
                
                # Добавляем медиафайлы
                for tale in metadata['tales']:
                    self._add_media_to_zip(zipf, tale)
                
                # Добавляем офлайн-читалку
                self._add_offline_reader(zipf)
            
            # Сохраняем пакет
            path = f"{self.base_dir}/{package_name}"
            default_storage.save(path, buffer)
            
            return path
            
        except Exception as e:
            logger.error(f"Failed to generate offline package: {str(e)}")
            raise

    def _prepare_metadata(self, tale_ids: list) -> dict:
        """Подготовка структурированных метаданных"""
        # Здесь должна быть логика получения данных из БД
        return {
            'version': '1.0',
            'generated_at': '2023-11-20',
            'tales': []  # Заполняется реальными данными
        }

    def _add_media_to_zip(self, zipf: zipfile.ZipFile, tale: dict):
        """Добавление медиафайлов в архив"""
        # Реализация загрузки и добавления файлов
        pass

    def _add_offline_reader(self, zipf: zipfile.ZipFile):
        """Добавление HTML-читалки в пакет"""
        reader_path = Path(__file__).parent / 'static/offline_reader'
        for file in reader_path.glob('*'):
            zipf.write(file, f"reader/{file.name}")