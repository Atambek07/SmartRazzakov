from PIL import Image, ImageOps
from io import BytesIO
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ImageOptimizer:
    """Оптимизация изображений для веба и мобильных устройств"""
    
    def __init__(self):
        self.max_sizes = {
            'thumbnail': (400, 400),
            'mobile': (800, 800),
            'desktop': (1200, 1200)
        }
        self.quality = getattr(settings, 'IMAGE_QUALITY', 85)

    def optimize_image(self, image_data: bytes, target: str = 'mobile') -> bytes:
        """
        Оптимизация изображения:
        - Ресайз под целевое устройство
        - Сжатие с контролем качества
        - Конвертация в WebP
        """
        try:
            img = Image.open(BytesIO(image_data))
            
            # Автоматическая ориентация
            img = ImageOps.exif_transpose(img)
            
            # Ресайз с сохранением пропорций
            img.thumbnail(self.max_sizes[target])
            
            # Оптимизация
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=self.quality)
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Image optimization failed: {str(e)}")
            raise

    def generate_variants(self, original_path: str) -> dict:
        """Генерация вариантов изображения для разных устройств"""
        variants = {}
        with open(original_path, 'rb') as f:
            original_data = f.read()
            
            for target in ['thumbnail', 'mobile', 'desktop']:
                try:
                    variants[target] = self.optimize_image(original_data, target)
                except Exception as e:
                    logger.warning(f"Failed to generate {target} variant: {str(e)}")
        
        return variants