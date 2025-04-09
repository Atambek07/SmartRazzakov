class EduSpaceDomainError(Exception):
    """Base exception for EduSpace domain errors"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ContentValidationError(EduSpaceDomainError):
    """Raised when content validation fails"""

class EnrollmentError(EduSpaceDomainError):
    """Raised when enrollment process fails"""

class CourseCapacityError(EnrollmentError):
    """Raised when course capacity is exceeded"""

class DuplicateEnrollmentError(EnrollmentError):
    """Raised when student is already enrolled"""

class ContentPublishingError(EduSpaceDomainError):
    """Raised when content publishing fails"""