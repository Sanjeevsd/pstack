from django.apps import AppConfig


class LoginRegisterConfig(AppConfig):
    name = "login_register"

    def ready(self):
        import login_register.signals
