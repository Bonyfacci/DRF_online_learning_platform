from django.urls import path

from app_school.apps import AppSchoolConfig
from rest_framework.routers import DefaultRouter

from app_school.views.cource import CourseViewSet
from app_school.views.lesson import LessonCreateAPIView, LessonListAPIView, LessonDetailAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView
from app_school.views.payments import PaymentsListAPIView
from app_school.views.subscription import SubscriptionListAPIView, SubscriptionCreateAPIView, SubscriptionUpdateAPIView, \
    SubscriptionDestroyAPIView

app_name = AppSchoolConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete'),

    # payments
    path('payments/', PaymentsListAPIView.as_view(), name='payments'),

    # subscriptions
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateAPIView.as_view(), name='subscription_update'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls
