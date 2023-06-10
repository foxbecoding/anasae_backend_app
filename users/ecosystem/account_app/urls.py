from rest_framework.routers import DefaultRouter
from users.ecosystem.account_app.views import *

router = DefaultRouter()
router.register(r"account-sign-up", AccountSignUpViewSet, basename="account-sign-up")
router.register(r"account-log-in", AccountLogInViewSet, basename="account-log-in")
router.register(r"account-log-out", AccountLogOutViewSet, basename="account-log-out")
urlpatterns = router.urls