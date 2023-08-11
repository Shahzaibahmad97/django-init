from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.defaults import server_error
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.core.views import error404
from api.jwtauth.views import CustomResetPasswordValidateToken, CustomResetPasswordConfirm, \
    CustomResetPasswordRequestToken
from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Homme API",
        default_version='v1',
        description="Here magic happens",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shahzaib.ahmad97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
admin.site.site_url = "https://www.google.com"

handler404 = error404

router = DefaultRouter()

urls = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),  # noqa
        name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa
    re_path(r'^', include(router.urls)),
    re_path(r'^redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa
    re_path(r'^api/forgot/validate_token', CustomResetPasswordValidateToken.as_view(),
        name="reset-password-validate"),
    re_path(r'^api/forgot/confirm', CustomResetPasswordConfirm.as_view(), name="reset-password-confirm"),
    re_path(r'^api/forgot', CustomResetPasswordRequestToken.as_view(), name="reset-password-request"),
    path('api/', include('api.urls')),
    path('admin', admin.site.urls)
]

urlpatterns = urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
