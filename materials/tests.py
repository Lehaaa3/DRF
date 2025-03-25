from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create(
            email='test@bk.ru',
            first_name='Test',
            last_name='Test',
            is_staff=True,
            is_active=True,
        )
        self.user.set_password('testpassword')

        self.course = Course.objects.create(
            title='Test_course',
            description='Test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test_lesson',
            description='Test_lesson',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_getting_lessons_list(self):
        """
            Тестирование получения списка уроков
        """
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 1, 'next': None, 'previous': None, 'results': [
            {'title': 'Test_lesson', 'description': 'Test_lesson', 'course': 4, 'url': None}]})

    def test_getting_lesson_detail(self):
        """
            Тестирование получения конкретного урока
        """
        url = reverse("materials:lesson-detail", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'title': 'Test_lesson', 'description': 'Test_lesson', 'course': 3, 'url': None})

    def test_create_lesson(self):
        """
            Тестирование создания урока
        """
        url = reverse("materials:lesson-create")
        data = {
            "title": "TEST",
            "description": "TEST",
            "course": self.course.pk,
            "owner": self.user.pk
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'title': 'TEST', 'description': 'TEST', 'course': 1, 'url': None}
                         )

    def test_update_lesson(self):
        """
            Тестирование редактирования урока
        """
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        data = {
            "title": "TEST_UPDATE",
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'title': 'TEST_UPDATE', 'description': 'Test_lesson', 'course': 5, 'url': None})

    def test_delete_lesson(self):
        """
            Тестирование удаления урока
        """

        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(description='Test_lesson').count(), 0)


class SubscriptionForCourseTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create(
            email='test@bk.ru',
            first_name='Test',
            last_name='Test',
            is_staff=True,
            is_active=True,
        )
        self.user.set_password('testpassword')

        self.course = Course.objects.create(
            title='Test_course',
            description='Test_course',
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """
            Тестирование подписки на курс.
        """

        url = f'/courses/{self.course.pk}/course_subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})

    def test_subscription_delete(self):
        """
            Тестирование удаления подписки на курс.
        """

        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        url = f'/courses/{self.course.pk}/course_subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})
