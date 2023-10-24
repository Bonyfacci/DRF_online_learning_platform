from datetime import timezone, datetime

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_school.models import Lesson
from app_school.paginators import LessonPaginator
from app_school.permissions import IsModerator, IsOwner
from app_school.serializers.lesson import LessonSerializer
from app_school.services import check_subscription


class LessonDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        course = self.get_object().course
        if course:
            time_delta = datetime.now(timezone.utc) - course.updated_at
            course.updated_at = datetime.now(timezone.utc)
            course.save()
            if time_delta.seconds // 3600 > 4:
                serializer.save()
                return check_subscription(course)
        serializer.save()


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
