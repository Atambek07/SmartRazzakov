# modules/gov_connect/application/use_cases/voting.py
from uuid import UUID
from datetime import datetime
from ...domain.entities import VotingEntity, VoteEntity
from ...domain.services import VotingService
from ...infrastructure.repositories import VotingRepository
from core.utils.responses import ResponseSuccess, ResponseFailure

class VotingCreationUseCase:
    def __init__(self, repo: VotingRepository):
        self.repo = repo

    def create_voting(self, dto):
        try:
            voting = VotingEntity(
                title=dto.title,
                description=dto.description,
                options=dto.options,
                start_date=dto.start_date,
                end_date=dto.end_date,
                min_age=dto.min_age,
                residency_required=dto.residency_required
            )
            created = self.repo.create(voting)
            return ResponseSuccess({
                "voting_id": str(created.id),
                "access_code": created.access_code
            })
        except Exception as e:
            return ResponseFailure(f"Ошибка создания голосования: {str(e)}")

class VoteProcessingUseCase:
    def __init__(self, repo: VotingRepository, auth_service):
        self.repo = repo
        self.auth = auth_service

    def cast_vote(self, voting_id: UUID, user_id: UUID, option: str):
        try:
            # Проверка прав
            if not self._validate_voting_rights(voting_id, user_id):
                return ResponseFailure("Нет прав для голосования")

            # Проверка времени
            voting = self.repo.get_voting(voting_id)
            if datetime.now() < voting.start_date:
                return ResponseFailure("Голосование еще не началось")
            if datetime.now() > voting.end_date:
                return ResponseFailure("Голосование уже завершено")

            # Проверка уникальности
            if self.repo.has_user_voted(voting_id, user_id):
                return ResponseFailure("Вы уже проголосовали")

            vote = VoteEntity(
                voting_id=voting_id,
                user_id=user_id,
                option=option,
                timestamp=datetime.now()
            )
            self.repo.record_vote(vote)
            
            return ResponseSuccess({"message": "Голос учтен"})
        except Exception as e:
            return ResponseFailure(f"Ошибка голосования: {str(e)}")

    def _validate_voting_rights(self, voting_id: UUID, user_id: UUID) -> bool:
        voting = self.repo.get_voting(voting_id)
        user = self.auth.get_user_profile(user_id)
        
        if user.age < voting.min_age:
            return False
        if voting.residency_required and not user.is_resident:
            return False
            
        return True

class VotingResultsUseCase:
    def __init__(self, repo: VotingRepository):
        self.repo = repo

    def get_results(self, voting_id: UUID):
        try:
            results = self.repo.calculate_results(voting_id)
            return ResponseSuccess({
                "total_votes": results['total'],
                "options": results['options'],
                "voter_demographics": results.get('demographics', {})
            })
        except Exception as e:
            return ResponseFailure(f"Ошибка получения результатов: {str(e)}")