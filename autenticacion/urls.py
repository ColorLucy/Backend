from django.urls import path

from .views import UserLoginAPIView
from .views import UserLogoutAPIView
from .views import UserRegisterAPIView

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("signup/", UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
    path("refesh/", UserLogoutAPIView.as_view(), name="user_logout"),
]
