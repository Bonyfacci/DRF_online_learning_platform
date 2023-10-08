from django.contrib import admin

from app_school.models import Course, Lesson, Payments


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'link', 'course')
    list_filter = ('course', )
    search_fields = ('name', 'description', )


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'paid_course', 'paid_lesson', 'date_of_payment', 'payment_amount', 'payment_method')
    list_filter = ('user', 'paid_course', 'paid_lesson')
    search_fields = ('user', 'paid_course', 'paid_lesson')
