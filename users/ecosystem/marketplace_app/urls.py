from rest_framework.routers import DefaultRouter
from users.ecosystem.marketplace_app.views import MAUserViewSet

router = DefaultRouter()
router.register(r"ma-user", MAUserViewSet, basename="ma-user")
urlpatterns = router.urls