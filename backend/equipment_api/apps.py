"""
App configuration for Equipment API
"""
from django.apps import AppConfig

class EquipmentApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipment_api'
    verbose_name = 'Equipment API'

    def ready(self):
        # Auto-create superuser on deploy
        from django.contrib.auth.models import User
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                password="admin123",
                email="admin@example.com"
            )