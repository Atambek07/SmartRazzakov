from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .infrastructure.models import TaleContentModel
from .infrastructure.qr_service import QRService
from .infrastructure.storage import MediaStorage
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=TaleContentModel)
def validate_tale_content(sender, instance: TaleContentModel, **kwargs):
    """Валидация контента перед сохранением."""
    if not any([instance.audio_url, instance.text_content, instance.images]):
        raise ValidationError(
            "Контент должен содержать хотя бы один формат (аудио, текст или изображения)"
        )

@receiver(post_save, sender=TaleContentModel)
def generate_qr_code(sender, instance: TaleContentModel, created: bool, **kwargs):
    """
    Генерирует и сохраняет QR-код при создании новой истории.
    Если QR уже существует - обновляет его при изменении location_id.
    """
    if not created and not kwargs.get('update_fields'):
        return  # Пропускаем, если это не создание и не явное обновление

    qr_service = QRService()
    storage = MediaStorage(use_s3=True)  # Используем S3 для продакшена

    try:
        # Генерация QR-кода с URL вида: /tales/{id}?location={location_id}
        qr_data = qr_service.generate_qr_code(
            tale_id=str(instance.id),
            format_preference="audio"  # Дефолтный формат
        )
        
        # Сохранение в хранилище
        qr_path = f"qrcodes/tale_{instance.id}.png"
        instance.qr_code = storage.upload_image(qr_data, qr_path)
        instance.save(update_fields=['qr_code'])

        logger.info(f"QR-код сгенерирован для истории {instance.id}")
    except Exception as e:
        logger.error(f"Ошибка генерации QR для {instance.id}: {str(e)}")
        raise  # Повторно вызываем исключение для отмены транзакции