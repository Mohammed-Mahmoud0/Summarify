from django.urls import path
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
