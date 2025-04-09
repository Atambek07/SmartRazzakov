from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseNotifier(ABC):
    @abstractmethod
    async def send(
        self,
        user_id: str,
        message: Dict[str, Any],
        **kwargs
    ) -> bool:
        pass
    
    def format_message(
        self,
        template: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'title': template.format(**context),
            'content': context.get('details', '')
        }