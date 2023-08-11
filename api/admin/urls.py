from rest_framework.routers import DefaultRouter

from api.admin.views import AdminUserViewSets

router = DefaultRouter(trailing_slash=False)
router.register(r'users', AdminUserViewSets, basename='admin_users')
urlpatterns = router.urls
