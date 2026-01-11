from rest_framework import viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrAdmin  # Импортируем ваш класс разрешений

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsModeratorOrAdmin()]  # Доступ только для модераторов или администраторов
        return [permissions.IsAuthenticated()]  # Остальные действия для аутентифицированных пользователей

class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]  # Аутентифицированные пользователи могут видеть список уроков

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Привязываем урок к текущему пользователю

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsModeratorOrAdmin()]  # Доступ только для модераторов или администраторов для редактирования и удаления
        return [permissions.IsAuthenticated()]  # Остальные действия для аутентифицированных пользователей

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав редактировать этот объект.")
        serializer.save()  # Сохраняем изменения

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав удалить этот объект.")
        instance.delete()  # Удаляем урок
