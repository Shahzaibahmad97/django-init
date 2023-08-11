from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.jwtauth.views import RegistrationViewSet
from api.users.views import partial_update, UserViewSets
from api.salons.views import SalonViewSets, StylistViewSets


router = DefaultRouter(trailing_slash=False)
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'users', UserViewSets, basename='users')
router.register(r'salons/stylists', StylistViewSets, basename='stylists')
router.register(r'salons', SalonViewSets, basename='salons')

urlpatterns = router.urls + [
    path('me', partial_update, name='partial_update'),
    path('admin/', include('api.admin.urls'), name='admin'),
    path('auth/', include('api.jwtauth.urls'), name='auth'),
]
