from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.feedback'

    def ready(self):
        from . import signals
        from .tasks import update_ratings_task