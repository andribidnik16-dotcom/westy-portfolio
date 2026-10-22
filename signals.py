
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import (
    pre_save,
    post_save,
    post_delete,
)
from django.dispatch import receiver

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def prepare_user_data(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.strip().lower()

    if instance.pk:
        logger.info(f'Оновлення користувача: {instance.username}')
    else:
        logger.info(f'Підготовка нового користувача: {instance.username}')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    profile = Profile.objects.create(user=instance)

    logger.info(
        'Створено профіль для користувача %s',
        instance.username
    )

    print(f'Профіль створено: {profile}')

    if instance.email:
        send_mail(
            subject='Ласкаво просимо!',
            message=(
                f'Привіт, {instance.first_name or instance.username}! '
                'Ваш обліковий запис успішно створено.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        logger.info(
            'Лист-підтвердження відправлено для %s',
            instance.email
        )
@receiver(post_delete, sender=User)
def user_deleted_cleanup(sender, instance, **kwargs):
    logger.info(
        'Користувача %s видалено',
        instance.username
    )

    print(f'Користувача видалено: {instance.username}')