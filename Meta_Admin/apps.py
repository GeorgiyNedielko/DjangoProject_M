from django.apps import AppConfig


class MetaAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Meta_Admin'

    def ready(self):
        import Meta_Admin.signals
