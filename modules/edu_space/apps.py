from django.apps import AppConfig

class EduSpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.edu_space'
    verbose_name = 'Образовательное пространство'

    def ready(self):
        # Импорт сигналов и других компонентов при инициализации
        import modules.edu_space.signals  # noqa
        from .infrastructure.integrations import payment_gateway
        payment_gateway.initialize()