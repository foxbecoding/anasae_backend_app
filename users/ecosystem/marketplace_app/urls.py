from rest_framework.routers import DefaultRouter
from users.ecosystem.marketplace_app.views import *

router = DefaultRouter()
router.register(r"mpa-user", MPAUserViewSet, basename="mpa-user")
router.register(r"mpa-user-profile", MPAUserProfileViewSet, basename="mpa-user-profile")
router.register(r"mpa-user-profile-image", MPAUserProfileImageViewSet, basename="mpa-user-profile-image")
urlpatterns = router.urls