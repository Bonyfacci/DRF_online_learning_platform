from rest_framework import serializers

from app_school.models import Course, Lesson
from app_school.serializers.lesson import LessonSerializer
from app_school.serializers.subscription import SubscriptionSerializer


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source='lessons', many=True, read_only=True)
    is_subscribed = SubscriptionSerializer(source='subscriptions', many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
