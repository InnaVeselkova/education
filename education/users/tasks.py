from .models import User
from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def deactivate_inactive_users():
    cutoff_date = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=cutoff_date, is_active=True)
    count = users_to_deactivate.update(is_active=False)
    return f"Deactivated {count} users."