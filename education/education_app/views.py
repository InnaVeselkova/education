from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrAdmin, IsNotModeratorOrAdmin, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Модераторы и администраторы не могут изменять курсы
        if self.action == 'create':
            permission_classes = [IsNotModeratorOrAdmin]
        # Модераторы, администраторы и владельцы могут просматривать и редактировать курсы
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsModeratorOrAdmin | IsOwner]
        # Только владельцы могут удалять курсы
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        # Остальные действия для всех авторизированных пользователей
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated] # Доступ только для аутентифицированных пользователей


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner] # Доступ только для владельцев курса

    def perform_create(self, serializer):
        # Устанавливаем владельца для нового урока
        serializer.save(owner=self.request.user)


class LessonDetail(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для аутентифицированных пользователей


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrAdmin, IsOwner]  # Доступ только для владельцев, модераторов и администраторов

    def perform_update(self, serializer):
        serializer.save()


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]  # Доступ только для владельцев уроков

    def perform_destroy(self, instance):
        instance.delete()

