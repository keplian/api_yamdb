from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/titles', TitlesViewSet, basename='TitlesView')

urlpatterns = [
    path('', include(router_v1.urls)),
]
