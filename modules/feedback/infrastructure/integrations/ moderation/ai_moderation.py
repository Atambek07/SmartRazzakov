# modules/feedback/infrastructure/integrations/moderation/ai_moderation.py
import requests
from core.config import settings
from core.logging import logger

class AIModerationService:
    def __init__(self):
        self.api_url = settings.MODERATION_API_URL
        self.api_key = settings.MODERATION_API_KEY
    
    def moderate_text(self, text: str) -> dict:
        """Модерация текста через AI API"""
        try:
            response = requests.post(
                f"{self.api_url}/text",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"text": text},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Moderation API error: {str(e)}")
            return {"status": "error", "decision": "pending"}

    def moderate_media(self, media_urls: list) -> dict:
        """Модерация изображений/видео"""
        results = {}
        for url in media_urls:
            try:
                response = requests.post(
                    f"{self.api_url}/image",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"url": url},
                    timeout=10
                )
                results[url] = response.json()
            except Exception as e:
                logger.error(f"Media moderation failed for {url}: {str(e)}")
                results[url] = {"status": "error"}
        return results

    def full_moderation(self, review_data: dict) -> dict:
        """Комплексная модерация отзыва"""
        result = {
            "text": self.moderate_text(review_data.get('text', '')),
            "media": self.moderate_media(review_data.get('media', []))
        }
        return self._make_decision(result)

    def _make_decision(self, results: dict) -> dict:
        """Принятие итогового решения на основе всех проверок"""
        if any([res.get('decision') == 'reject' for res in results['media'].values()]):
            return {"final_decision": "reject", "reason": "invalid_media"}
        
        if results['text'].get('decision') == 'reject':
            return {"final_decision": "reject", "reason": results['text'].get('reason')}
        
        return {"final_decision": "approve"}