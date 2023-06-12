from rest_framework.routers import DefaultRouter
from users.ecosystem.marketplace_app.views import MAUserViewSet, MAUserProfileViewSet

router = DefaultRouter()
router.register(r"ma-user", MAUserViewSet, basename="ma-user")
router.register(r"ma-user-profile", MAUserProfileViewSet, basename="ma-user-profile")
urlpatterns = router.urls