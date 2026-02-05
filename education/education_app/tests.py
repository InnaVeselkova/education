from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Course, Lesson, Subscription
from users.models import User

class LessonListTests(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.owner_user = User.objects.create_user(email='owner@example.com', password='ownerpass')
        self.admin_user = User.objects.create_user(email='admin@example.com', password='adminpass', is_staff=True)

        # Создаем курс и урок
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson Description',
            course=self.course,
            owner=self.owner_user
        )
        print(f"[LessonListTests setUp] User count: {User.objects.count()},"
              f" Course count: {Course.objects.count()}, Lesson count: {Lesson.objects.count()}")

    def test_get_lessons_authenticated(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('education_app:lesson-list')  # имя маршрута, как в urls.py
        response = self.client.get(url)
        print(f"[LessonListTests test_get_lessons_authenticated] Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "Доступ к урокам должен быть разрешен для аутентифицированных пользователей.")

    def test_get_lessons_unauthenticated(self):
        url = reverse('education_app:lesson-list')  # имя маршрута, как в urls.py
        response = self.client.get(url)
        print(f"[LessonListTests test_get_lessons_unauthenticated] Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         "Доступ к урокам должен быть запрещен для неаутентифицированных пользователей.")


class LessonTestsUpdate(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.owner_user = User.objects.create_user(email='owner@example.com', password='ownerpass')
        self.moderator_user = User.objects.create_user(email='moderator@example.com', password='modpass', is_staff=True)
        self.other_user = User.objects.create_user(email='other@example.com', password='otherpass')

        # Создаем курс и урок
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson Description',
            course=self.course,
            owner=self.owner_user
        )
        print(f"[LessonTestsUpdate setUp] User count: {User.objects.count()},"
              f" Course count: {Course.objects.count()}, Lesson count: {Lesson.objects.count()}")

    def test_update_lesson(self):
        update_data = {
            'title': 'Обновленное название урока',
            'description': 'Обновленное описание',
            'course': self.course.id,
            'video_url': 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }

        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.put(
            reverse('education_app:lesson_update', args=[self.lesson.id]),
            update_data,
            format='json'
        )
        print(f"[LessonTestsUpdate test_update_lesson] Moderator Status: {response.status_code}")
        print(f"[LessonTestsUpdate test_update_lesson] Moderator DATA: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "Модераторы должны иметь возможность обновлять уроки.")

        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(
            reverse('education_app:lesson_update', args=[self.lesson.id]),
            update_data,
            format='json'
        )
        print(f"[LessonTestsUpdate test_update_lesson] Other user Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         "Обычные пользователи не должны иметь возможность обновлять уроки.")



class LessonDeleteTests(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.owner_user = User.objects.create_user(email='owner@example.com', password='owner')
        self.moderator_user = User.objects.create_user(email='moderator@example.com', password='modpass', is_staff=True)
        self.other_user = User.objects.create_user(email='other@example.com', password='otherpass')

        # Создаем курс и урок
        self.course = Course.objects.create(title='Test1 Course', description='Test1 Description', owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title='Test1 Lesson',
            description='Lesson1 Description',
            course=self.course,
            owner=self.owner_user
        )
        print(f"[LessonDeleteTests setUp] User count: {User.objects.count()},"
              f" Course count: {Course.objects.count()}, Lesson count: {Lesson.objects.count()}")

    def test_delete_lesson_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(reverse('education_app:lesson_delete', args=[self.lesson.id]))
        print(f"[LessonDeleteTests test_delete_lesson_as_moderator] Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         "Модераторы не должны удалять уроки.")

    def test_delete_lesson_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('education_app:lesson_delete', args=[self.lesson.id]))
        print(f"[LessonDeleteTests test_delete_lesson_as_other_user] Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         "Обычные пользователи не могут удалять уроки.")

    def test_delete_lesson_as_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(reverse('education_app:lesson_delete', args=[self.lesson.id]))
        print(f"[LessonDeleteTests test_delete_lesson_as_owner] Status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         "Владелец должен иметь возможность удалять уроки.")


class LessonDetail(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.owner_user = User.objects.create_user(email='owner@example.com', password='ownerpass')
        self.other_user = User.objects.create_user(email='other@example.com', password='otherpass')
        self.anon_user = None  # Неаутентифицированный пользователь

        # Создание курса и урока
        self.course = Course.objects.create(title='Курс', description='desc', owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title='Урок',
            description='desc',
            course=self.course,
            owner=self.owner_user
        )
        self.detail_url = reverse('education_app:lesson-detail', args=[self.lesson.id])
        self.delete_url = reverse('education_app:lesson-detail', args=[self.lesson.id])

    def test_lesson_detail_authenticated(self):
        """Аутентифицированный пользователь может получить детали урока"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.lesson.id)

    def test_lesson_detail_unauthenticated(self):
        """Неаутентифицированный пользователь получает 401"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonCreateTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.owner_user = User.objects.create_user(email='owner@example.com', password='ownerpass')
        self.moderator_user = User.objects.create_user(email='moderator@example.com', password='modpass', is_staff=True)
        self.admin_user = User.objects.create_user(email='admin@example.com', password='adminpass', is_staff=True)

        # Создаем курс (владелец курса может быть любым; для тестов достаточно-owner)
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.owner_user)

        # URL создания урока (на основе списка, если у вас CreateAPIView в списке)
        self.create_url = reverse('education_app:lesson-create')

        self.base_data = {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'course': self.course.id,
            'video_url': 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }

    def test_create_lesson_as_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        resp = self.client.post(self.create_url, self.base_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_as_moderator_forbidden(self):
        """Модераторы не должны иметь доступ к созданию урока."""
        self.client.force_authenticate(user=self.moderator_user)
        resp = self.client.post(self.create_url, self.base_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_admin_forbidden(self):
        """Администраторы не должны иметь доступ к созданию урока."""
        self.client.force_authenticate(user=self.admin_user)
        resp = self.client.post(self.create_url, self.base_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_unauthenticated_forbidden(self):
        """Неавторизованный пользователь не может создавать уроки."""
        resp = self.client.post(self.create_url, self.base_data, format='json')
        # Обычно 401 Unauthorized, может быть 403 в зависимости от конфигурации
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class SubscriptionViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.course = Course.objects.create(
            title='Test Course',
            owner=self.user
        )

    def test_add_subscription(self):
        """
        Проверка добавления подписки
        """
        url = reverse('education_app:subscription')
        response = self.client.post(url, {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        """
        Проверка удаления подписки
        """
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('education_app:subscription')
        response = self.client.post(url, {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_requires_authentication(self):
        """
        Проверка, что без аутентификации доступ запрещен
        """
        self.client.logout()
        url = reverse('education_app:subscription')
        response = self.client.post(url, {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
