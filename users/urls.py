from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
]
