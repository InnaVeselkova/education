from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from education_app.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Зашифровать пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


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

    objects = CustomUserManager()

    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
        ('stripe', 'Stripe')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пользователя
    owner = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)  # Владелец платежа
    payment_date = models.DateTimeField(auto_now_add=True)  # Дата и время оплаты
    paid_course = models.ForeignKey(Course, null=True, blank=True,
                               on_delete=models.SET_NULL)  # Ссылка на оплаченный курс (может быть пустым)
    paid_lesson = models.ForeignKey(Lesson, null=True, blank=True,
                               on_delete=models.SET_NULL)  # Ссылка на оплаченный урок (может быть пустым)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма оплаты
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)  # Способ оплаты

    stripe_product_id = models.CharField(max_length=200,
                                         blank=True,
                                         null=True)
    stripe_price_id = models.CharField(max_length=200,
                                       blank=True,
                                       null=True)
    stripe_session_id = models.CharField(max_length=200,
                                         blank=True,
                                         null=True)
    checkout_url = models.URLField(blank=True,
                                   null=True)

    def __str__(self):
        return f"Платеж {self.id} от {self.user} за {self.amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
