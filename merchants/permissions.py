from rest_framework.permissions import BasePermission
from merchants.models import Merchant

class IsMerchantPermission(BasePermission):
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists()    

    def has_object_permission(self, request, view, obj) -> bool:
        print(Merchant.objects.filter(user_id=str(request.user.id)).exists())
        return Merchant.objects.filter(user_id=str(request.user.id)).exists()