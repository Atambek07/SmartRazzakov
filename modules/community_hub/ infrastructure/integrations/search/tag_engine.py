# modules/community_hub/infrastructure/integrations/search/tag_engine.py
import re
import logging
from typing import List, Dict
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from . import TagEngine

logger = logging.getLogger(__name__)


class CommunityTagEngine(TagEngine):
    """Движок для работы с тегами сообщества"""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=10000
        )
        self.tag_freq = Counter()
        self.tag_cooccurrence = {}
        self.all_tags = set()

    async def extract_tags(self, text: str, top_n: int = 5) -> List[str]:
        """Извлечение тегов из текста с помощью TF-IDF"""
        try:
            # Очистка текста
            clean_text = re.sub(r'[^\w\s]', '', text.lower())

            # Векторизация текста
            tfidf_matrix = self.vectorizer.fit_transform([clean_text])
            feature_names = self.vectorizer.get_feature_names_out()

            # Получение важных терминов
            sorted_items = self._sort_coo(tfidf_matrix.tocoo())
            keywords = [feature_names[idx] for idx in sorted_items[:top_n]]

            # Обновление статистики
            self._update_tag_stats(keywords)

            return keywords
        except Exception as e:
            logger.error(f"Tag extraction failed: {str(e)}")
            return []

    async def suggest_tags(self, prefix: str, limit: int = 5) -> List[str]:
        """Подсказки тегов по префиксу"""
        prefix = prefix.lower()
        suggestions = [
            tag for tag in self.all_tags
            if tag.startswith(prefix)
        ]
        # Сортировка по частоте использования
        suggestions.sort(key=lambda x: self.tag_freq.get(x, 0), reverse=True)
        return suggestions[:limit]

    async def related_tags(self, tags: List[str]) -> Dict[str, List[str]]:
        """Поиск связанных тегов"""
        result = {}
        for tag in tags:
            related = self.tag_cooccurrence.get(tag, {})
            sorted_related = sorted(
                related.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            result[tag] = [t[0] for t in sorted_related]
        return result

    def _sort_coo(self, coo_matrix):
        """Сортировка элементов TF-IDF матрицы"""
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def _update_tag_stats(self, tags: List[str]):
        """Обновление статистики тегов"""
        for tag in tags:
            self.tag_freq[tag] += 1
            self.all_tags.add(tag)

        # Обновление совместной встречаемости
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                pair = (tags[i], tags[j])
                if pair[0] not in self.tag_cooccurrence:
                    self.tag_cooccurrence[pair[0]] = {}
                if pair[1] not in self.tag_cooccurrence[pair[0]]:
                    self.tag_cooccurrence[pair[0]][pair[1]] = 0
                self.tag_cooccurrence[pair[0]][pair[1]] += 1