from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from keybert import KeyBERT
import logging
import re
import mimetypes
from django.core.files.storage import default_storage
from .exceptions import MediaProcessingError

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


def get_media_type(filename: str) -> str:
    """Определение типа медиа по расширению"""
    mime, _ = mimetypes.guess_type(filename)
    if not mime:
        raise MediaProcessingError(f"Can't detect media type for {filename}")

    if mime.startswith('video/'):
        return 'video'
    elif mime.startswith('audio/'):
        return 'audio'
    elif mime in ['model/gltf-binary', 'application/octet-stream']:
        return '3d_model'
    else:
        return 'other'


def validate_media_size(file, max_size_mb: int = 100):
    """Проверка размера файла"""
    if file.size > max_size_mb * 1024 * 1024:
        raise MediaProcessingError(f"File exceeds maximum size {max_size_mb}MB")
