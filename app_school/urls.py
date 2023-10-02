from django.urls import path

from app_school.apps import AppSchoolConfig
from rest_framework.routers import DefaultRouter

from app_school.views.cource import CourseViewSet
from app_school.views.lesson import LessonCreateAPIView, LessonListAPIView, LessonDetailAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView

app_name = AppSchoolConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete'),
] + router.urls
