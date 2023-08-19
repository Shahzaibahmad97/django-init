from rest_framework.routers import DefaultRouter

from api.admin.views import AdminUserViewSets, AdminCategoryViewSets, AdminProductTypeViewSets, AdminVendorViewSets, AdminProductViewSets, AdminProductImageViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', AdminUserViewSets, basename='admin_users')

router.register(r'categories', AdminCategoryViewSets, basename='admin_categories')
router.register(r'product-types', AdminProductTypeViewSets, basename='admin_product_types')
router.register(r'vendors', AdminVendorViewSets, basename='admin_vendors')
router.register(r'products/images', AdminProductImageViewSet, basename='products_images')
router.register(r'products', AdminProductViewSets, basename='products')

urlpatterns = router.urls
