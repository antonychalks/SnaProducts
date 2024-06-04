from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    # noinspection PyUnresolvedReferences
    def ready(self):
        import checkout.signals
