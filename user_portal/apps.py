from django.apps import AppConfig


class UserPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_portal'
    
    def ready(self):
        import user_portal.signals   # Import your signals when the app is ready
