from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .paginators import CustomPageNumberPagination
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsModeratorOrAdmin, IsNotModeratorOrAdmin, IsOwner
from .tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Передаем текущий запрос в контекст
        return context

    def perform_update(self, serializer):
        course = serializer.save()
        subscriptions = Subscription.objects.select_related('user').filter(course=course)
        for subscription in subscriptions:
            user_email = subscription.user.email
            course_title = course.title
            send_course_update_email.delay(user_email, course_title)


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated] # Доступ только для аутентифицированных пользователей
    pagination_class = CustomPageNumberPagination


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotModeratorOrAdmin] # Нет доступа для администраторов и модераторов

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
    permission_classes = [IsModeratorOrAdmin | IsOwner]  # Доступ только для владельцев, модераторов и администраторов

    def perform_update(self, serializer):
        serializer.save()


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]  # Доступ только для владельцев уроков

    def perform_destroy(self, instance):
        instance.delete()


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        # Проверяем, есть ли у пользователя подписка на курс
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Если подписка существует, удаляем ее
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки нет, создаем новую
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message})
