from rest_framework.routers import DefaultRouter
from categories.ecosystem.marketplace_app.views import *

router = DefaultRouter()
router.register(r"mpa-categories", MPACategoryViewSet, basename="mpa-category")
urlpatterns = router.urls