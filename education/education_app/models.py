from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to="course_images/",  blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=6)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Курс"
        verbose_name_plural="Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="lesson_images/",  blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

    class Meta:
        verbose_name="Урок"
        verbose_name_plural="Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')  # Обеспечим уникальность подписки на курс для каждого пользователя
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
