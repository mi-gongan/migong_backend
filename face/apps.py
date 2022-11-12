from django.apps import AppConfig
from .services import Face


class FaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'face'

    def ready(self) -> None:
        Face.__init__(Face)
        return super().ready()
