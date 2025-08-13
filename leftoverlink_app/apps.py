from django.apps import AppConfig

class LeftoverlinkAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leftoverlink_app'

    def ready(self):
        import leftoverlink_app.signals
