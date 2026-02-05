from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from .views import CourseViewSet, LessonList, LessonDetail, LessonCreate, LessonUpdate, LessonDelete, SubscriptionView

app_name = 'education_app'

# Создание маршрутизатора для ViewSet
router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Все маршруты для курсов
    path('lessons/', LessonList.as_view(), name='lesson-list'),  # Список уроков
    path('lessons/create/', LessonCreate.as_view(), name='lesson-create'),  # Создание нового урока
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),  # Просмотр конкретного урока
    path('lessons/<int:pk>/update/', LessonUpdate.as_view(), name='lesson_update'),  # Обновление конкретного урока
    path('lessons/<int:pk>/delete/', LessonDelete.as_view(), name='lesson_delete'),  # Удаление конкретного урока
    path('subscriptions/', SubscriptionView.as_view(), name='subscription'),
]
