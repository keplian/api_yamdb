from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as vs
from .serializers import MyTokenObtainPairView
from .views import email_auth

router_v1 = routers.DefaultRouter()
# <<<<<<< HEAD
# router_v1.register(r'auth/email', vs.UserModelViewSet, basename='auth')
# router_v1.register(r'titles', vs.TitleModelViewSet, basename='title')
# router_v1.register(r'titles/(?P<id>[0-9]+)/reviews',
#                    vs.ReviewModelViewSet, basename='review')
# =======
router_v1.register(r"titles", vs.TitleModelViewSet, basename="title")
router_v1.register(
    r"titles/(?P<id>[0-9]+)/reviews", vs.ReviewModelViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments",
    vs.CommentModelViewSet,
    basename="comment",
)

urlpatterns = [
    re_path(r"^v1/", include(router_v1.urls)),
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
