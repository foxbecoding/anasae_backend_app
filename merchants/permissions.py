from rest_framework.permissions import BasePermission
from merchants.models import Merchant
from users.models import User

SAFE_METHODS = ['GET', 'POST']

class IsMerchantPermission(BasePermission):
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return False     

    def has_object_permission(self, request, view, obj) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists()
