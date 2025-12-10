from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.contenttypes.models import ContentType

from Meta_Admin.models import Project, Task, Tag, ProjectFile


class Command(BaseCommand):
    help = "Создаёт группы Manager, Client и Developer и назначает им нужные права."

    def handle(self, *args, **options):
        #  создаём группы (если их ещё нет)
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        client_group, _ = Group.objects.get_or_create(name="Client")
        developer_group, _ = Group.objects.get_or_create(name="Developer")

        #_ — флаг, создана ли она (True/False), он нам не нужен.

        # --- content types для моделей ---
        ct_group = ContentType.objects.get_for_model(AuthGroup)
        ct_permission = ContentType.objects.get_for_model(Permission)
        ct_user = ContentType.objects.get_for_model(User)

        ct_project = ContentType.objects.get_for_model(Project)
        ct_projectfile = ContentType.objects.get_for_model(ProjectFile)
        ct_tag = ContentType.objects.get_for_model(Tag)
        ct_task = ContentType.objects.get_for_model(Task)

        # маленький хелпер
        def perms(ct, actions):
            """
            ct – ContentType модели,
            actions – список строк: ['add', 'change', 'delete', 'view']
            """
            codes = [f"{action}_{ct.model}" for action in actions]
            return list(Permission.objects.filter(content_type=ct, codename__in=codes))

        # ====== PERMISSIONS ======

        # --- права Manager ---

        manager_perms = []

        # Группы / разрешения / пользователи
        manager_perms += Permission.objects.filter(
            content_type=ct_group,
            codename__in=["view_group"]
        )
        manager_perms += Permission.objects.filter(
            content_type=ct_permission,
            codename__in=["view_permission", "add_permission"]
        )
        manager_perms += Permission.objects.filter(
            content_type=ct_user,
            codename__in=["add_user", "view_user"]
        )

        # Project, ProjectFile, Tag, Task
        manager_perms += perms(ct_project, ["add", "change", "delete", "view"])
        manager_perms += perms(ct_projectfile, ["add", "change", "delete", "view"])
        manager_perms += perms(ct_tag, ["add", "change", "view"])
        manager_perms += perms(ct_task, ["add", "change", "view"])

        manager_group.permissions.set(manager_perms)

        # --- права Client ---

        client_perms = []

        # Пользователи: создавать, изменять, просматривать
        client_perms += Permission.objects.filter(
            content_type=ct_user,
            codename__in=["add_user", "change_user", "view_user"]
        )

        # Проекты: полный CRUD
        client_perms += perms(ct_project, ["add", "change", "delete", "view"])

        # Файлы проектов: только создавать и просматривать
        client_perms += perms(ct_projectfile, ["add", "view"])

        # Теги: полный CRUD
        client_perms += perms(ct_tag, ["add", "change", "delete", "view"])

        # Задачи: полный CRUD
        client_perms += perms(ct_task, ["add", "change", "delete", "view"])

        client_group.permissions.set(client_perms)

        # --- права Developer ---

        developer_perms = []

        # Пользователи: полный CRUD
        developer_perms += Permission.objects.filter(
            content_type=ct_user,
            codename__in=["add_user", "change_user", "delete_user", "view_user"]
        )

        # Проекты: полный CRUD
        developer_perms += perms(ct_project, ["add", "change", "delete", "view"])

        # Файлы проектов: полный CRUD
        developer_perms += perms(ct_projectfile, ["add", "change", "delete", "view"])

        # Теги: полный CRUD
        developer_perms += perms(ct_tag, ["add", "change", "delete", "view"])

        # Задачи: полный CRUD
        developer_perms += perms(ct_task, ["add", "change", "delete", "view"])

        developer_group.permissions.set(developer_perms)

        self.stdout.write(self.style.SUCCESS("Группы Manager, Client, Developer настроены."))

