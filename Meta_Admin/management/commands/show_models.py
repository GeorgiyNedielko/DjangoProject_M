from django.core.management.base import BaseCommand
from django.apps import apps
import inspect
import os


class Command(BaseCommand):
    help = "Показывает все модели, их поля, связи и расположение файлов"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=== Список всех приложений и моделей ==="))

        for app_config in apps.get_app_configs():
            self.stdout.write(f"\n\n📦 Приложение: {app_config.label}")
            self.stdout.write("-" * 60)

            for model in app_config.get_models():
                model_name = model.__name__
                file_path = inspect.getfile(model)

                self.stdout.write(f"\n🟦 Модель: {model_name}")
                self.stdout.write(f"📁 Файл: {file_path}")

                # Выводим поля
                self.stdout.write("   📌 Поля:")
                for field in model._meta.get_fields():

                    field_type = field.__class__.__name__
                    line = f"      • {field.name} ({field_type})"

                    # ForeignKey, OneToOne, ManyToMany: добавляем информацию о связи
                    if field.is_relation:
                        related_model = (
                            field.related_model.__name__
                            if field.related_model
                            else "Unknown"
                        )
                        line += f" → {related_model}"

                        # FK: выводим поведение on_delete
                        if field.many_to_one:
                            line += f" [ForeignKey]"
                        elif field.one_to_one:
                            line += f" [OneToOne]"
                        elif field.many_to_many:
                            line += f" [ManyToMany]"

                    self.stdout.write(line)

        self.stdout.write(self.style.SUCCESS("\n=== Готово! ==="))
