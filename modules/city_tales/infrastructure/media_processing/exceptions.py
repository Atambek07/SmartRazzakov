class MediaProcessingError(Exception):
    """Базовое исключение для ошибок обработки"""
    pass

class InvalidVideoFormatError(MediaProcessingError):
    """Неподдерживаемый видеоформат"""
    def __init__(self, format: str):
        self.format = format
        super().__init__(f"Unsupported video format: {format}")

class ModelOptimizationError(MediaProcessingError):
    """Ошибка оптимизации 3D-модели"""
    pass

class SubtitleGenerationError(MediaProcessingError):
    """Ошибка создания субтитров"""
    pass