from django.apps import AppConfig


class PluslifeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pluslife'

    def ready(self):
        import pluslife.signals