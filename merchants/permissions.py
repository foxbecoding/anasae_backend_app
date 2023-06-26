from rest_framework.permissions import BasePermission
from merchants.models import Merchant, MerchantSubcription
import stripe

class MerchantPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        SAFE_METHODS = ('GET', 'POST')
        if request.method in SAFE_METHODS:
            return True
        return False    

    def has_object_permission(self, request, view, obj) -> bool:
        uid = obj['uid']
        
        if Merchant.objects.filter(user_id=str(request.user.id)).exists() == False:
            return False
        
        if Merchant.objects.filter(uid=uid).exists() == False:
            return False
        
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        if Merchant_Instance.uid != uid:
            return False
        
        return True

class MerchantPaymentMethodPermission(BasePermission):

    message = "Access Denied!"
    
    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists()        
    
class MerchantSubscriptionPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj) -> bool:
        # Merchant_Instance = Merchant.objects.get(user_id=request.user.id)
        # if MerchantSubcription.objects.filter(merchant_id=Merchant_Instance.id).exists() == False:
        #     return False

        if MerchantSubcription.objects.filter(pk=obj['pk']).exists() == False:
            return False
        # Merchant_Subcription_Instance = MerchantSubcription.objects.get(pk=obj['pk'])
        # print(Merchant_Subcription_Instance.merchant_id)
        # Merchant_Subcription_Instance = MerchantSubcription.objects.get(merchant_id=Merchant_Instance.id)
        # print(str(Merchant_Subcription_Instance.id))
        return True