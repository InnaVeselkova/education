from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from .views import CourseViewSet, LessonList, LessonDetail

app_name='education_app'

# Создание маршрутизатора для ViewSet
router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Все маршруты для курсов
    path("lessons/", LessonList.as_view(), name="lesson-list"),  # Список и создание
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),  # Получение, изменение и удаление
]
