from rest_framework.routers import DefaultRouter
from .views import ValidationViewSet

router = DefaultRouter()
router.register(r'validations', ValidationViewSet, basename='validations')

urlpatterns = router.urls