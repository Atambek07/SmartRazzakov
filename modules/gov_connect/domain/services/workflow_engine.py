# modules/gov_connect/domain/services/workflow_engine.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from uuid import UUID

class WorkflowEngine(ABC):
    """Абстрактный класс движка рабочих процессов"""
    
    @abstractmethod
    def start_process(
        self,
        process_key: str,
        entity_id: UUID,
        init_variables: Dict[str, Any]
    ) -> str:
        pass
    
    @abstractmethod
    def handle_event(self, process_id: str, event_name: str, payload: dict):
        pass

class CamundaWorkflowEngine(WorkflowEngine):
    """Реализация для Camunda BPMN"""
    
    def __init__(self, camunda_client):
        self.client = camunda_client

    def start_process(self, process_key: str, entity_id: UUID, variables: dict):
        return self.client.start_process(
            process_key,
            business_key=str(entity_id),
            variables=variables
        )

    def handle_event(self, process_id: str, event_name: str, payload: dict):
        self.client.correlate_message(
            message_name=event_name,
            process_instance_id=process_id,
            process_variables=payload
        )

class GovConnectWorkflow:
    """Фасад для управления workflow"""
    
    def __init__(self, engine: WorkflowEngine, repo):
        self.engine = engine
        self.repo = repo

    def initiate_complaint_flow(self, complaint_id: UUID):
        complaint = self.repo.find_by_id(complaint_id)
        return self.engine.start_process(
            process_key="complaint_processing",
            entity_id=complaint_id,
            variables={
                "category": complaint.category,
                "priority": self._calculate_priority(complaint)
            }
        )

    def _calculate_priority(self, complaint) -> int:
        """Рассчитывает приоритет на основе категории и истории"""
        base_priority = {
            'roads': 3,
            'lighting': 2,
            'utilities': 1
        }.get(complaint.category, 0)
        
        similar_count = self.repo.count_similar_complaints(complaint)
        return base_priority + min(similar_count, 3)