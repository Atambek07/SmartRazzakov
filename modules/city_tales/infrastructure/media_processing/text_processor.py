from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from keybert import KeyBERT
from .exceptions import MediaProcessingError
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, language: str = "russian"):
        self.language = language
        self.summarizer = LsaSummarizer()
        self.keyword_model = KeyBERT()

    def process(self, text: str, summary_sentences: int = 3) -> dict:
        """Основной метод обработки текста"""
        try:
            return {
                'summary': self.summarize(text, summary_sentences),
                'keywords': self.extract_keywords(text),
                'clean_text': self.clean_text(text)
            }
        except Exception as e:
            logger.error(f"Text processing failed: {str(e)}")
            raise MediaProcessingError("Text processing error")

    def summarize(self, text: str, sentences: int) -> str:
        """Суммаризация текста с использованием LSA"""
        parser = PlaintextParser.from_string(text, Tokenizer(self.language))
        summary = self.summarizer(parser.document, sentences)
        return " ".join(str(s) for s in summary)

    def extract_keywords(self, text: str, top_n: int = 5) -> list:
        """Извлечение ключевых фраз с помощью KeyBERT"""
        return [
            kw[0] for kw in
            self.keyword_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words=self.language,
                top_n=top_n
            )
        ]

    def clean_text(self, text: str) -> str:
        """Базовая очистка текста"""
        # Реализация цензуры и нормализации
        return text