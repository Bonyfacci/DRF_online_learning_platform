from django.db.models import Count
from rest_framework import viewsets

from app_school.models import Course
from app_school.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
