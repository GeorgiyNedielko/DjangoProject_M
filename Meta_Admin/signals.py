from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Task


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)



@receiver(pre_save, sender=Task)
def remember_old_status(sender, instance, **kwargs):
    """
    Перед сохранением задачи запоминаем старый статус,
    чтобы в post_save понимать – реально ли он изменился.
    """
    if not instance.pk:

        instance._old_status = None
        return

    try:
        old_obj = Task.objects.get(pk=instance.pk)
        instance._old_status = old_obj.status
    except Task.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Task)
def send_status_change_email(sender, instance, created, **kwargs):
    """
    После сохранения задачи отправляем письмо владельцу,
    если статус действительно изменился.
    Новые задачи (created=True) НЕ уведомляем.
    """
    if created:
        # при создании задачи письмо не шлём (можно включить, если нужно)
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status


    if old_status == new_status:
        return

    owner = getattr(instance, "owner", None)
    if not owner or not owner.email:
        # некому отправлять
        return

    subject = f"Статус вашей задачи «{instance.title}» изменился"


    message_lines = [
        f"Здравствуйте, {owner.username}!",
        "",
        f"Статус вашей задачи «{instance.title}» был изменён.",
        f"Старый статус: {old_status or '—'}",
        f"Новый статус: {new_status}",
        "",
        "Это тестовое уведомление, отправленное с учебного Django сервера.",
    ]
    message = "\n".join(message_lines)

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
        [owner.email],
        fail_silently=True,
    )
