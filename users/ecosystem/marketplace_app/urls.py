from rest_framework.routers import DefaultRouter
from users.ecosystem.marketplace_app.views import MPAUserViewSet, MPAUserProfileViewSet

router = DefaultRouter()
router.register(r"mpa-user", MPAUserViewSet, basename="mpa-user")
router.register(r"mpa-user-profile", MPAUserProfileViewSet, basename="mpa-user-profile")
urlpatterns = router.urls