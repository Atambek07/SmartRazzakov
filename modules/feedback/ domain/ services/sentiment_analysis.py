# modules/feedback/domain/services/sentiment_analysis.py
from transformers import pipeline
from typing import Optional

class AISentimentAnalyzer:
    def __init__(self):
        self._model = None
        self._tokenizer = None

    def load_model(self):
        """Ленивая загрузка модели"""
        if not self._model:
            self._model = pipeline(
                "sentiment-analysis",
                model="cointegrated/rubert-tiny-sentiment-balanced"
            )

    def analyze(self, text: str) -> dict:
        self.load_model()
        result = self._model(text)[0]
        
        label_map = {
            'neutral': 0,
            'positive': 1,
            'negative': -1
        }
        
        return {
            'label': result['label'],
            'score': result['score'] * label_map[result['label']]
        }

class HybridSentimentAnalyzer:
    def __init__(self, ai_analyzer: AISentimentAnalyzer):
        self.ai = ai_analyzer

    def analyze(self, text: str) -> dict:
        """Комбинированный анализ с правилами"""
        ai_result = self.ai.analyze(text)
        
        # Дополнительные правила
        if '!' in text:
            ai_result['score'] *= 1.2
        if '?' in text:
            ai_result['score'] *= 0.8
        
        return ai_result