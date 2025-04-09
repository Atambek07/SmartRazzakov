# modules/edu_space/application/use_cases/content_management.py
from uuid import UUID
from ...domain.entities import EducationalContent
from ...domain.repositories import ContentRepository
from ..dto.content_dto import (
    ContentUploadRequest,
    ContentResponse,
    TestSubmission
)

class ContentService:
    def __init__(self, content_repo: ContentRepository):
        self.content_repo = content_repo

    def upload_content(self, request: ContentUploadRequest) -> ContentResponse:
        content = EducationalContent(
            id=UUID(int=0),
            title=request.title,
            content_type=request.content_type,
            subject=request.subject,
            grade_level=request.grade_level,
            author_id=request.author_id,
            file_url=request.file_url,
            metadata={
                'interactive_config': request.interactive_config
            }
        )
        
        saved_content = self.content_repo.save(content)
        return ContentResponse(
            id=saved_content.id,
            title=saved_content.title,
            type=saved_content.content_type,
            preview_url=saved_content.file_url,
            author_name=self._get_author_name(saved_content.author_id),
            rating=0.0,
            difficulty="Medium",
            interactive_available=bool(saved_content.metadata.get('interactive_config')),
            created_at=saved_content.created_at
        )

    def grade_test(self, submission: TestSubmission) -> dict:
        content = self.content_repo.get_by_id(submission.content_id)
        correct_answers = content.metadata.get('answer_key', {})
        
        score = self._calculate_score(
            submission.answers,
            correct_answers
        )
        
        return {
            "score": score,
            "total_questions": len(correct_answers),
            "correct_answers": self._get_correct_answers(submission.answers, correct_answers)
        }

    def _get_author_name(self, author_id: UUID) -> str:
        # Implementation would call user service
        return "Author Name"

    def _calculate_score(self, answers: dict, correct: dict) -> float:
        correct_count = sum(1 for k, v in answers.items() if correct.get(k) == v)
        return round(correct_count / len(correct) * 100, 2)

    def _get_correct_answers(self, answers: dict, correct: dict) -> dict:
        return {k: correct.get(k) for k in answers.keys()}