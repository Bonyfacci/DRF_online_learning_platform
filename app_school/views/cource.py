from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app_school.models import Course
from app_school.paginators import CoursePaginator
from app_school.permissions import IsModerator, IsOwner
from app_school.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'CREATE':
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action in ['LIST', 'update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()
