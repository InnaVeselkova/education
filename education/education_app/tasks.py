from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_course_update_email(user_email, course_title):
    subject = f"Обновление курса: {course_title}"
    message = f"Здравствуйте! В курсе '{course_title}' произошли изменения. Подробнее ознакомьтесь на сайте."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )