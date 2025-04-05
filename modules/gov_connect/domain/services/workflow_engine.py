from ..entities import ComplaintStatus, ComplaintPriority


class ComplaintWorkflow:
    @staticmethod
    def determine_priority(complaint_data: dict) -> ComplaintPriority:
        """Определяет приоритет жалобы на основе контента"""
        if 'авария' in complaint_data['title'].lower():
            return ComplaintPriority.HIGH
        elif 'ремонт' in complaint_data['description'].lower():
            return ComplaintPriority.MEDIUM
        return ComplaintPriority.LOW

    def process_complaint(self, complaint: 'CitizenComplaint') -> None:
        """Автоматически обрабатывает новую жалобу"""
        complaint.priority = self.determine_priority({
            'title': complaint.title,
            'description': complaint.description
        })

        if complaint.priority == ComplaintPriority.HIGH:
            complaint.assigned_department = "emergency"
            complaint.status = ComplaintStatus.IN_PROGRESS