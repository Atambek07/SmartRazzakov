from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import json
import logging

logger = logging.getLogger(__name__)


class SubtitleGenerator:
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def generate_srt(self, audio_path: str, language: str = "ru") -> str:
        """Генерация субтитров в формате SRT"""
        try:
            audio = AudioSegment.from_file(audio_path)
            recognizer = KaldiRecognizer(self.model, 16000)
            recognizer.SetWords(True)

            # Обработка аудио
            results = []
            for i in range(0, len(audio), 10000):  # Чанки по 10 секунд
                chunk = audio[i:i + 10000]
                data = chunk.raw_data
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    results.extend(result.get('result', []))

            # Формирование SRT
            srt_content = []
            for i, word in enumerate(results):
                start = word['start']
                end = word['end']
                text = word['word']
                srt_content.append(
                    f"{i + 1}\n"
                    f"{self._format_time(start)} --> {self._format_time(end)}\n"
                    f"{text}\n"
                )

            return "\n".join(srt_content)
        except Exception as e:
            logger.error(f"Subtitle generation failed: {str(e)}")
            raise

    def _format_time(self, seconds: float) -> str:
        """Форматирование времени для SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"