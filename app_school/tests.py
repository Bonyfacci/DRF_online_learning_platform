from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_school.models import Course, Lesson, Subscription
from app_school.serializers.subscription import SubscriptionSerializer
from users.models import User


class LessonListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test'
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )
        self.lesson = Lesson.objects.create(
            title="lesson_test",
            description="test",
            course=self.course,
            owner=self.user
        )

    def test_get_list(self):
        """ Тест для получения списка уроков """

        self.client.force_authenticate(
            user=self.user
        )
        response = self.client.get(
            reverse('app_school:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "link": self.lesson.link,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "photo": self.lesson.photo,
                        "course": self.lesson.course_id,
                        "owner": self.lesson.owner_id
                    }
                ]
            }
        )


class LessonCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
            is_staff=True
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )

    def test_lesson_create(self):
        """ Тест для создания урока """

        self.client.force_authenticate(
            user=self.user
        )
        data = {
            'title': 'lesson_test',
            'course': self.course.id,
            'link': 'https://www.youtube.com/video'
        }

        response = self.client.post(
            reverse('app_school:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "link": "https://www.youtube.com/video",
                "title": "lesson_test",
                "description": None,
                "photo": None,
                "course": self.course.id,
                "owner": None
            }
        )

    def test_lesson_create_validation_error(self):
        """ Тест для создания урока с некорректной ссылкой """

        self.client.force_authenticate(
            user=self.user
        )
        data = {
            'title': 'lesson_test',
            'course': self.course.id,
            'link': 'https://google.com'
        }

        response = self.client.post(
            reverse('app_school:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'link': ['Ссылка курса или урока должна быть на Youtube']}
        )


class LessonUpdateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
            is_staff=True
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )
        self.lesson = Lesson.objects.create(
            title="lesson_test",
            description="test",
            link="https://www.youtube.com/video",
            course=self.course,
            owner=self.user
        )

    def test_lesson_update(self):
        """ Тест для изменения урока """

        self.client.force_authenticate(
            user=self.user
        )
        data = {
            'title': 'lesson_test_update',
            'description': 'test_update',
            'link': 'https://www.youtube.com/video_update'
        }

        response = self.client.patch(
            reverse(
                'app_school:lesson_update',
                args=[self.lesson.id]),
            data=data
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.title,
            'lesson_test_update'
        )
        self.assertEqual(
            self.lesson.link,
            'https://www.youtube.com/video_update'
        )
        self.assertEqual(
            self.lesson.description,
            'test_update'
        )

    def test_lesson_update_validation_error(self):
        """ Тест для изменения урока с некорректной ссылкой """

        self.client.force_authenticate(
            user=self.user
        )
        data = {
            'title': 'lesson_test_update',
            'description': 'test_update',
            'link': 'https://www.google.com/video_update'
        }

        response = self.client.patch(
            reverse(
                'app_school:lesson_update',
                args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'link': ['Ссылка курса или урока должна быть на Youtube']}
        )


class LessonDetailTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )
        self.lesson = Lesson.objects.create(
            title="lesson_test",
            description="test",
            link="https://www.youtube.com/video",
            course=self.course,
            owner=self.user
        )

    def test_lesson_retrieve(self):
        """ Тест для просмотра урока """

        self.client.force_authenticate(
            user=self.user
        )
        response = self.client.get(
            reverse('app_school:lesson_get',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve_wrong_user(self):
        """ Тест на запрет просмотр урока, если пользователь - не владелец """

        new_user = User.objects.create(
            email='test_other@sky.pro',
            password='test',
        )
        self.client.force_authenticate(
            user=new_user
        )
        response = self.client.get(
            reverse('app_school:lesson_get',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class LessonDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )
        self.lesson = Lesson.objects.create(
            title="lesson_test",
            description="test",
            link="https://www.youtube.com/video",
            course=self.course,
            owner=self.user
        )

    def test_delete_lesson(self):
        """ Тест для удаления урока """

        self.client.force_authenticate(
            user=self.user
        )
        response = self.client.delete(
            reverse('app_school:lesson_delete',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Lesson.objects.filter(id=self.lesson.id).exists()
        )

    def test_delete_lesson_wrong_user(self):
        """ Тест на запрет удаления урока, если пользователь - не владелец """

        new_user = User.objects.create(
            email='test_other@sky.pro',
            password='test',
        )
        self.client.force_authenticate(
            user=new_user
        )
        response = self.client.get(
            reverse('app_school:lesson_get',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        response = self.client.delete(
            reverse('app_school:lesson_delete',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
        )
        self.course = Course.objects.create(
            title="course_test",
            description="test"
        )

    def test_list_subscriptions(self):
        """ Тест списка подписок """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('app_school:subscription_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        subscriptions = Subscription.objects.filter(user=self.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)

        self.assertEqual(
            response.data,
            serializer.data
        )

    def test_create_subscription(self):
        """ Тест для создания подписки """

        self.client.force_authenticate(
            user=self.user
        )
        data = {
            'user': self.user.id,
            'course': self.course.id,
            'subscription': True
        }

        response = self.client.post(
            reverse('app_school:subscription_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Subscription.objects.count(),
            1
        )

        subscription = Subscription.objects.get()

        self.assertEqual(
            subscription.user,
            self.user
        )
        self.assertEqual(
            subscription.course,
            self.course
        )
        self.assertEqual(
            subscription.subscription,
            True
        )

    def test_delete_subscription(self):
        """ Тест удаления подписки """

        self.client.force_authenticate(user=self.user)

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            subscription=True
        )

        response = self.client.delete(
            reverse('app_school:subscription_delete',
                    args=[self.subscription.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Subscription.objects.count(),
            0
        )

