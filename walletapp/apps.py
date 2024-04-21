from django.apps import AppConfig


class WalletappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'walletapp'

    def ready(self):
        from walletapp import signals