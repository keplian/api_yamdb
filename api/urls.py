from django.urls import include, re_path
from rest_framework import routers

from . import views as vs

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', vs.TitleModelViewSet, basename='title')
router_v1.register(r'titles/(?P<title_id>[0-9]+)/reviews', vs.ReviewModelViewSet,
                   basename='review')
urlpatterns = [
    re_path(r'^v1/', include(router_v1.urls)),
]
