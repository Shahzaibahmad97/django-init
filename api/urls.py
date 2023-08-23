from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.jwtauth.views import RegistrationViewSet
from api.users.views import partial_update, UserViewSets
from api.salons.views import SalonViewSets, StylistViewSets
from api.product_types.views import ProductTypeViewSet
from api.categories.views import CategoryViewSet
from api.vendors.views import VendorViewSet
from api.products.views import ProductViewSets

from api.support.views import FeedbackViewSets, ContactUsViewSets


router = DefaultRouter(trailing_slash=False)
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'users', UserViewSets, basename='users')
router.register(r'salons/stylists', StylistViewSets, basename='stylists')
router.register(r'salons', SalonViewSets, basename='salons')

router.register(r'product-types', ProductTypeViewSet, basename='product_types')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'products', ProductViewSets, basename='products')

router.register(r'contact-us', ContactUsViewSets, basename='contact_us')
router.register(r'feedback', FeedbackViewSets, basename='feedback')

urlpatterns = router.urls + [
    path('me', partial_update, name='partial_update'),
    path('admin/', include('api.admin.urls'), name='admin'),
    path('auth/', include('api.jwtauth.urls'), name='auth'),
]
