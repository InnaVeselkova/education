from rest_framework import viewsets
from rest_framework import generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# ViewSet для Курсов
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Generic-классы для Уроков
class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

