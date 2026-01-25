from dateutil.relativedelta import relativedelta

from .models import User
from celery import shared_task
from django.utils import timezone


@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - relativedelta(months=1)
    users_to_deactivate = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = users_to_deactivate.update(is_active=False)
    return f"Deactivated {count} users."