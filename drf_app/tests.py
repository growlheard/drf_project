from rest_framework.test import APITestCase
from rest_framework import status

from drf_app.models import Lesson
from users.models import User


class BaseTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(
            email='admin@gmail.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password('qwerty')
        self.user.save()
        response = self.client.post(
            '/users/token/', {'email': 'admin@gmail.com', 'password': 'qwerty'})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class LessonTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.lesson = Lesson.objects.create(
            id='3',
            name='Тест_имя',
            description='Тест_описание',
            video='https://www.youtube.com'
        )

    def test_create_lesson(self):
        """ Тестирование создания урока"""
        response = self.client.post('/lessons/create/', {'name': 'Тест_имя',
                                                         'description': 'Тест_имя',
                                                         'video': 'https://www.youtube.com'})
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_all_lessons(self):
        """ Получение всех уроков """
        response = self.client.get(
            '/lessons/'
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """ Удаление урока """
        response = self.client.delete(
            '/lessons/delete/3/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_retrieve(self):
        """ Изменение урока """
        response = self.client.get(
            '/lessons/3/'
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class SubscriptionTest(BaseTestCase):
    def test_create_subscription(self):
        response = self.client.post(
            '/subscription/create/',
            {
                "status": "True",
                "user": "1",
                "course": "1"
            }
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
