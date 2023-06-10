from rest_framework.routers import DefaultRouter
from users.ecosystem.auth_management_app.views import *

router = DefaultRouter()
router.register(r"user-sign-up", UserSignUpViewSet, basename="user-sign-up")
router.register(r"user-log-in", UserLogInViewSet, basename="user-log-in")
router.register(r"user-log-out", UserLogOutViewSet, basename="user-log-out")
urlpatterns = router.urls