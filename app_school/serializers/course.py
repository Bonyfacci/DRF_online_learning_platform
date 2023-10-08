from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from app_school.models import Course, Lesson
from app_school.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source='lessons', many=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
