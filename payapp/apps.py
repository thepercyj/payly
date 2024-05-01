from django.apps import AppConfig


class PayappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payapp'

    # calling instance signals to be executed after post operation for UserProfile
    def ready(self):
        from payapp import signals