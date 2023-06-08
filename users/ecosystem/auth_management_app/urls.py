from rest_framework.routers import DefaultRouter
from users.ecosystem.auth_management_app.views import UserSignUpViewSet

router = DefaultRouter()
router.register(r"user-sign-up", UserSignUpViewSet, basename="user-sign-up")
urlpatterns = router.urls