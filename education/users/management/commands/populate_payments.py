from django.core.management.base import BaseCommand
from users.models import User, Payment
from education_app.models import Course, Lesson
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the Payments table with sample data'

    def handle(self, *args, **kwargs):
        # Список данных о платежах
        payments_data = [
            {
                "user_id": 1,
                "payment_date": timezone.now(),
                "paid_course_id": 1,
                "paid_lesson_id": 4,
                "amount": 100.00,
                "payment_method": 'cash'
            },
            {
                "user_id": 2,
                "payment_date": timezone.now(),
                "paid_course_id": 2,
                "paid_lesson_id": 5,
                "amount": 200.00,
                "payment_method": 'transfer'
            }
        ]

        # Добавление каждого платежа в базу данных
        for payment_data in payments_data:
            user = User.objects.get(id=payment_data["user_id"])
            course = Course.objects.get(id=payment_data["paid_course_id"])
            lesson = Lesson.objects.get(id=payment_data["paid_lesson_id"])

            payment = Payment.objects.create(
                user=user,
                payment_date=payment_data["payment_date"],
                paid_course=course,
                paid_lesson=lesson,
                amount=payment_data["amount"],
                payment_method=payment_data["payment_method"]
            )

            self.stdout.write(self.style.SUCCESS(f'Payment created: {payment}'))
