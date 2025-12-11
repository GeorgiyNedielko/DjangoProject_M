from django.apps import AppConfig


class MetaAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Meta_Admin'

    def ready(self):
        import Meta_Admin.signals


from django.apps import AppConfig


class MetaAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Meta_Admin"

    def ready(self):
        # импортируем сигналы при старте приложения
        import Meta_Admin.signals