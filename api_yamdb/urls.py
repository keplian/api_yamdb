from django.contrib import admin
from django.urls import include, path

urlpatterns = [
# <<<<<<< HEAD
#     path('api/v1/auth/token/', TokenObtainPairView.as_view(),
#          name='token_obtain_pair'),
#     path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(),
#          name='token_refresh'),
#     path('admin/', admin.site.urls),
#     path('api/', include('api.urls')),
#     path(
#         'redoc/',
#         TemplateView.as_view(template_name='redoc.html'),
#         name='redoc'
#     ),
# =======
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),

]
