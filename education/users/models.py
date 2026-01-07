from django.contrib.auth.models import AbstractUser
from django.db import models

from education.education_app.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите вашу почту"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Фотография",
        help_text="Загрузите фотографию",
    )
    city = models.CharField(max_length=25, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пользователя
    payment_date = models.DateTimeField(auto_now_add=True)  # Дата и время оплаты
    course = models.ForeignKey(Course, null=True, blank=True,
                               on_delete=models.CASCADE)  # Ссылка на оплаченный курс (может быть пустым)
    lesson = models.ForeignKey(Lesson, null=True, blank=True,
                               on_delete=models.CASCADE)  # Ссылка на оплаченный урок (может быть пустым)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма оплаты
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)  # Способ оплаты

    def __str__(self):
        payment_method_display = self.get_payment_method_display() if self.payment_method else 'Неизвестный способ'
        return f"Платеж от {self.user.username} - сумма: {self.amount} ({payment_method_display})"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
