from datetime import datetime, timezone

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app_school.models import Course
from app_school.paginators import CoursePaginator
from app_school.permissions import IsModerator, IsOwner
from app_school.serializers.course import CourseSerializer
from app_school.services import check_subscription


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        time_delta = datetime.now(timezone.utc) - self.get_object().updated_at
        course = serializer.save()
        if time_delta.seconds // 3600 > 4:
            return check_subscription(course)

    def get_permissions(self):
        if self.action == 'CREATE':
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action in ['LIST', 'update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()
