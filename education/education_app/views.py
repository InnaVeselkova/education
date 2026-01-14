from rest_framework import viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrAdmin  # Импортируем ваш класс разрешений

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Разрешение для всех действий - только для аутентифицированных пользователей
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Устанавливаем владельцем курса текущего пользователя
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()  # Получаем объект курса
        # Проверяем, является ли текущий пользователь владельцем курса
        if instance.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать этот объект.")
        serializer.save()

    def perform_destroy(self, instance):
        instance = self.get_object()  # Получаем объект курса
        # Проверяем, является ли текущий пользователь владельцем курса
        if instance.owner != self.request.user:
            raise PermissionDenied("У вас нет прав удалить этот объект.")
        instance.delete()

class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        # Все аутентифицированные пользователи могут видеть список уроков
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Модераторы и администраторы могут создавать уроки
        if self.request.user.is_staff or self.request.user.groups.filter(name='Модераторы').exists():
            serializer.save(owner=self.request.user)  # Привязываем урок к текущему пользователю
        else:
            raise PermissionDenied("У вас нет прав на создание уроков.")

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        # Разрешаем доступ всем аутентифицированным пользователям для получения деталей урока
        if self.request.method in ['PUT', 'PATCH']:
            # Модераторы и администраторы могут изменять уроки
            return [IsModeratorOrAdmin()]
        elif self.request.method == 'DELETE':
            # Только автор урока или администратор могут удалять уроки
            return [permissions.IsAdminUser()]  # Вызывается, чтобы только администраторы могли удалять
        return [permissions.IsAuthenticated()]  # Остальные действия для аутентифицированных пользователей

    def perform_update(self, serializer):
        instance = self.get_object()
        # Проверяем, является ли пользователь автором или администратором
        if instance.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав редактировать этот объект.")
        serializer.save()

    def perform_destroy(self, instance):
        # Проверяем, является ли пользователь автором урока или администратором
        if instance.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав удалить этот объект.")
        instance.delete()
