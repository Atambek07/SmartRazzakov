from better_profanity import profanity


class ProfanityFilter:
    def __init__(self):
        profanity.load_censor_words()

    def check_text(self, text: str) -> bool:
        """Проверяет текст на ненормативную лексику"""
        return profanity.contains_profanity(text)

    def censor_text(self, text: str) -> str:
        """Заменяет нецензурные слова"""
        return profanity.censor(text)