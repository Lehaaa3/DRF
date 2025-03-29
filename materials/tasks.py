from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_mail_for_subscribers(course, user_list: list):
    try:
        send_mail(
            subject='Обновление курса',
            message=f"Курс '{course}' обновлен!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[*user_list],
            fail_silently=False
        )
    except Exception as error:
        print(error)


@shared_task
def check_last_login():
    one_month_ago = timezone.now() - timedelta(days=30)
    print(one_month_ago)
    print(f"TIME_ZONE setting: {settings.TIME_ZONE}")
    print(f"USE_TZ setting: {settings.USE_TZ}")
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    ).update(is_active=False)

    null_logins = User.objects.filter(
        last_login=None,
        is_active=True
    ).update(is_active=False)

    print(f'Deactivated {inactive_users} users and {null_logins} null login users.')
