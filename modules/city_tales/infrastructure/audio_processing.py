import os
import logging
from pydub import AudioSegment
from django.conf import settings
from .storage import MediaStorage

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Обработка аудиофайлов: нормализация, конвертация, метаданные"""
    
    def __init__(self):
        self.storage = MediaStorage()
        self.supported_formats = ['mp3', 'wav', 'ogg']
        self.target_bitrate = getattr(settings, 'AUDIO_BITRATE', '128k')

    def process_audio(self, file_path: str) -> dict:
        """
        Основной метод обработки:
        - Конвертация в целевой формат
        - Нормализация громкости
        - Извлечение метаданных
        """
        try:
            # Загрузка файла из хранилища
            audio_file = self.storage.open(file_path)
            audio = AudioSegment.from_file(audio_file)
            
            # Нормализация громкости
            audio = self._normalize_audio(audio)
            
            # Конвертация
            processed_audio = self._convert_audio(audio)
            
            # Сохранение результата
            new_path = f"processed/{os.path.splitext(file_path)[0]}.mp3"
            self.storage.save(new_path, processed_audio)
            
            return {
                'status': 'success',
                'path': new_path,
                'duration': len(audio) / 1000,  # в секундах
                'bitrate': self.target_bitrate
            }
            
        except Exception as e:
            logger.error(f"Audio processing failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _normalize_audio(self, audio: AudioSegment) -> AudioSegment:
        """Нормализация громкости до -16dB LUFS"""
        target_dBFS = -16.0
        change_in_dBFS = target_dBFS - audio.dBFS
        return audio.apply_gain(change_in_dBFS)

    def _convert_audio(self, audio: AudioSegment) -> BytesIO:
        """Конвертация в MP3 с целевым битрейтом"""
        buffer = BytesIO()
        audio.export(buffer, format="mp3", bitrate=self.target_bitrate)
        buffer.seek(0)
        return buffer

    def extract_metadata(self, file_path: str) -> dict:
        """Извлечение метаданных из аудиофайла"""
        # Реализация с использованием mutagen или аналогичной библиотеки
        pass