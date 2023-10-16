from rest_framework import serializers

from app_school.models import Lesson
from app_school.validators import link_validator


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(validators=[link_validator])

    class Meta:
        model = Lesson
        fields = '__all__'
