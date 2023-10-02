from django.contrib import admin

from app_school.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'link', 'course')
    list_filter = ('course', )
    search_fields = ('name', 'description', )
