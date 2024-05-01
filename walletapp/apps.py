from django.apps import AppConfig


class WalletappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'walletapp'

    # calling instance signals to be executed after post operation for creating wallet for new users
    def ready(self):
        from walletapp import signals