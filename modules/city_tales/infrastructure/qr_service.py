import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import logging
from urllib.parse import urlencode
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class QRGenerationError(Exception):
    """Кастомное исключение для ошибок генерации QR"""
    pass

class QRService:
    """
    Сервис для генерации QR-кодов с динамическими URL.
    Поддерживает:
    - Настройку базового URL через Django settings
    - Параметры для формата контента и локации
    - Кастомизацию дизайна QR
    - Сохранение в разные хранилища
    """

    def __init__(self):
        self.base_url = getattr(settings, 'QR_BASE_URL', 'https://citytales.example.com')
        self.default_params = {
            'utm_source': 'qr_code',
            'utm_medium': 'print'
        }

    def build_tale_url(self, tale_id: str, location_id: str, format_preference: Optional[str] = None) -> str:
        """
        Генерирует URL для QR-кода с параметрами:
        - tale_id: UUID истории
        - location_id: ID достопримечательности
        - format_preference: предпочитаемый формат контента
        """
        params = {
            'tale_id': tale_id,
            'location_id': location_id,
            **self.default_params
        }

        if format_preference:
            params['format'] = format_preference

        return f"{self.base_url}/tales/content?{urlencode(params)}"

    def generate_qr_code(
        self,
        tale_id: str,
        location_id: str,
        format_preference: Optional[str] = None,
        design_options: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Генерирует QR-код в виде бинарных данных PNG.
        
        Параметры:
        - tale_id: UUID истории
        - location_id: ID локации
        - format_preference: аудио/текст/визуал
        - design_options: {
            'size': 12,          # Размер модуля
            'border': 2,         # Размер границы
            'color': '#1a237e',  # Цвет QR
            'bg_color': '#ffffff'# Фон
        }
        """
        try:
            # Формируем URL
            url = self.build_tale_url(tale_id, location_id, format_preference)
            
            # Настройки дизайна
            options = {
                'version': 3,
                'error_correction': qrcode.constants.ERROR_CORRECT_H,
                'box_size': design_options.get('size', 10) if design_options else 10,
                'border': design_options.get('border', 2) if design_options else 2,
            }

            # Генерация QR
            qr = qrcode.QRCode(**options)
            qr.add_data(url)
            qr.make(fit=True)

            # Применяем цвет если указан
            fill_color = design_options.get('color', '#000000') if design_options else 'black'
            back_color = design_options.get('bg_color', '#ffffff') if design_options else 'white'

            img = qr.make_image(
                fill_color=fill_color,
                back_color=back_color
            )

            # Конвертация в PNG
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"QR generation failed: {str(e)}")
            raise QRGenerationError(f"Could not generate QR: {str(e)}")

    def generate_and_save_qr(
        self,
        tale_id: str,
        location_id: str,
        storage,
        format_preference: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Генерирует QR и сохраняет в указанное хранилище.
        Возвращает путь к сохранённому файлу.
        
        Параметры:
        - storage: экземпляр Django Storage (S3Boto3Storage и т.д.)
        - kwargs: дополнительные параметры для generate_qr_code()
        """
        try:
            qr_data = self.generate_qr_code(
                tale_id=tale_id,
                location_id=location_id,
                format_preference=format_preference,
                **kwargs
            )
            
            # Сохраняем в хранилище
            file_path = f"qrcodes/tale_{tale_id}.png"
            storage.save(file_path, ContentFile(qr_data))
            
            return file_path

        except Exception as e:
            logger.error(f"QR save failed for tale {tale_id}: {str(e)}")
            raise QRGenerationError(f"Could not save QR: {str(e)}")

    @staticmethod
    def get_qr_url(file_path: str, storage) -> str:
        """Возвращает публичный URL QR-кода"""
        try:
            return storage.url(file_path)
        except Exception as e:
            logger.error(f"Could not get QR URL: {str(e)}")
            raise QRGenerationError(f"URL generation failed: {str(e)}")