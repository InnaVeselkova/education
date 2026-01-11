from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrAdmin  # Импорт нового класса разрешений

# ViewSet для Курсов
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]  # Только администраторы могут создавать и удалять курсы
        return [IsModeratorOrAdmin()]  # Просмотр и редактирование для модераторов и администраторов

# Generic-классы для Уроков
class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]  # Доступ к списку для всех аутентифицированных пользователей

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsModeratorOrAdmin()]  # Модераторы могут редактировать уроки
        elif self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]  # Только администраторы могут удалять уроки
        return super().get_permissions()  # Доступ для всех остальных действий
