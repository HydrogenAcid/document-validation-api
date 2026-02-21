# auth_app/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import ProfileView
# URL routing for authentication-related endpoints.
# These routes handle JWT token issuance and user profile access.

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view()),
    path("profile/", ProfileView.as_view()),
]