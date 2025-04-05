from django.apps import AppConfig


class HotNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.hot_news'

    def ready(self):
        from . import signals
        from .tasks import fetch_rss_feeds