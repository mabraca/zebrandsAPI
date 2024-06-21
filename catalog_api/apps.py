from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog_api'

    def ready(self):
        # Ensures that the signal handlers are registered when the application is ready
        import catalog_api.signals
