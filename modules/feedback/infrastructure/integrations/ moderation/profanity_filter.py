# modules/feedback/infrastructure/integrations/moderation/profanity_filter.py
import re
from typing import List
from core.config import settings

class ProfanityFilter:
    def __init__(self):
        self.banned_words = self._load_banned_words()
        self.replacement = settings.PROFANITY_REPLACEMENT
        self.patterns = self._generate_patterns()

    def _load_banned_words(self) -> List[str]:
        return [
            "мат1", "мат2", "мат3"  # Заменить реальными словами
        ]

    def _generate_patterns(self):
        substitutions = {
            'а': '[аa@]',
            'о': '[оo0]',
            'е': '[еe]',
            'и': '[иi]',
            'с': '[сc]',
            'к': '[кk]'
        }
        
        patterns = []
        for word in self.banned_words:
            pattern = ''.join([substitutions.get(c, c) for c in word])
            patterns.append(re.compile(pattern, re.IGNORECASE))
        
        return patterns

    def filter_text(self, text: str) -> str:
        for pattern in self.patterns:
            text = pattern.sub(self.replacement, text)
        return text

    def contains_profanity(self, text: str) -> bool:
        return any(pattern.search(text) for pattern in self.patterns)