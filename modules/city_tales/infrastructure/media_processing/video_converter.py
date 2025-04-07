from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from keybert import KeyBERT
import logging
import re
import subprocess
from pathlib import Path
from .exceptions import InvalidVideoFormatError
from .utils import validate_media_size
import logging
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.summarizer = LsaSummarizer()
        self.keyword_model = KeyBERT()

    def summarize(self, text: str, sentences_count: int = 3) -> str:
        """Автосуммаризация текста"""
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("russian"))
            summary = self.summarizer(parser.document, sentences_count)
            return " ".join([str(s) for s in summary])
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            return text[:500] + "..."  # Fallback

    def extract_keywords(self, text: str, top_n: int = 5) -> list:
        """Извлечение ключевых слов"""
        keywords = self.keyword_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words="russian",
            top_n=top_n
        )
        return [kw[0] for kw in keywords]

    def censor_text(self, text: str, forbidden_words: set) -> str:
        """Цензура запрещенных слов"""
        pattern = re.compile("|".join(forbidden_words), re.IGNORECASE)
        return pattern.sub("[CENSORED]", text)


class VideoConverter:
    FORMATS = {
        'hls': {
            'command': [
                'ffmpeg', '-i', '{input}', '-codec:', 'copy',
                '-hls_time', '10', '-hls_list_size', '0',
                '-f', 'hls', '{output}'
            ],
            'extension': '.m3u8'
        },
        'dash': {
            'command': [
                'ffmpeg', '-i', '{input}', '-map', '0',
                '-codec:', 'copy', '-f', 'dash',
                '-seg_duration', '10', '{output}'
            ],
            'extension': '.mpd'
        }
    }

    def convert(self, input_path: str, output_dir: str, format: str = 'hls') -> str:
        """Конвертация видео в адаптивный формат"""
        if format not in self.FORMATS:
            raise InvalidVideoFormatError(format)

        try:
            output_path = str(Path(output_dir) / f"stream{self.FORMATS[format]['extension']}")
            cmd = [part.format(input=input_path, output=output_path)
                   for part in self.FORMATS[format]['command']]

            subprocess.run(cmd, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise MediaProcessingError("Video conversion failed")
