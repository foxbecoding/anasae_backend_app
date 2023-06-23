from rest_framework.routers import DefaultRouter
from merchants.ecosystem.merchant_center_app.views import *

router = DefaultRouter()
router.register(r"mc-merchant", MCMerchantViewSet, basename="mc-merchant"),
router.register(r"mc-merchant-subscription", MCMerchantSubcriptionViewSet, basename="mc-merchant-subscription")
router.register(r"mc-merchant-payment-method", MCMerchantPaymentMethodViewSet, basename="mc-merchant-payment-method")
urlpatterns = router.urls