# modules/feedback/infrastructure/integrations/moderation/spam_detector.py
import re
from typing import Dict
from core.config import settings

class SpamDetector:
    def __init__(self):
        self.rules = {
            'links': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'emails': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'repetitions': re.compile(r'(\b\w+\b)(?:\s+\1){3,}', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict:
        results = {
            'spam_score': 0,
            'reasons': []
        }

        # Проверка ссылок
        links = self.rules['links'].findall(text)
        if len(links) > 2:
            results['spam_score'] += 30
            results['reasons'].append('too_many_links')

        # Проверка повторений
        if self.rules['repetitions'].search(text):
            results['spam_score'] += 40
            results['reasons'].append('repetitive_content')

        # Проверка электронных почт
        emails = self.rules['emails'].findall(text)
        if emails:
            results['spam_score'] += 20 * len(emails)
            results['reasons'].append('email_addresses')

        # Проверка капса
        if len(text) > 10 and sum(1 for c in text if c.isupper()) / len(text) > 0.5:
            results['spam_score'] += 20
            results['reasons'].append('excessive_caps')

        return results

    def is_spam(self, text: str, threshold=50) -> bool:
        analysis = self.analyze(text)
        return analysis['spam_score'] >= threshold