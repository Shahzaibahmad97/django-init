from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OTPViewSet, LoginViewSet, TokenRefreshView

router = DefaultRouter(trailing_slash=False)
router.register(r'otp', OTPViewSet, basename='otp')

urlpatterns = router.urls + [
    path('login', LoginViewSet.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

