from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(required=False)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"

    def validate(self, data):
        # Проверяем, есть ли video_url в переданных данных
        if 'video_url' in data:
            video_url = data['video_url']
            # Вызываем валидацию для video_url
            validate_video_url(video_url)
        return data


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # Поле для проверки подписки

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user  # Получаем текущего пользователя из контекста
        return Subscription.objects.filter(user=user, course=obj).exists()  # Проверяем, подписан ли пользователь на курс


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']
        read_only_fields = ['id', 'user']