from django.apps import AppConfig


class BookingPendingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_pending'

    def ready(self) -> None:
        import booking_pending.signals
