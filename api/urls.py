from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import MyTokenObtainPairView
from .views import email_auth

urlpatterns = [
    path(
        "redoc/",
        TemplateView.as_view(template_name="redoc.html"),
        name="redoc",
    ),
    path("v1/auth/email/", email_auth, name="email_auth"),
    path(
        "v1/token/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
