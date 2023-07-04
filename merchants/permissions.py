from rest_framework.permissions import BasePermission
from merchants.models import *
import stripe

class MerchantPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        SAFE_METHODS = ('GET', 'POST')
        if request.method in SAFE_METHODS:
            return True
        return False    

    def has_object_permission(self, request, view, obj) -> bool:
        pk = obj['pk']
        
        if not Merchant.objects.filter(user_id=str(request.user.id)).exists():
            return False
        
        if not Merchant.objects.filter(pk=pk).exists():
            return False
        
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        if str(Merchant_Instance.id) != str(pk):
            return False
        
        return True

class MerchantPaymentMethodPermission(BasePermission):

    message = "Access Denied!"
    
    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists()      

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if not MerchantPaymentMethod.objects.filter(pk__in=obj['pk']).exists():
                return False
        return True
    
class MerchantSubscriptionPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == 'POST':
            if 'merchant_plan' not in request.data: return False
            if 'payment_method' not in request.data: return False
            if 'price_key' not in request.data: return False
            
            if not MerchantPlan.objects.filter(pk=request.data['merchant_plan']).exists(): return False
            if not MerchantPlanPrice.objects.filter(stripe_price_key=request.data['price_key']): return False
            
            Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
            Merchant_Payment_Method_Instances = MerchantPaymentMethod.objects.filter(merchant_id=Merchant_Instance.id)
            payment_methods = [pm.stripe_pm_id for pm in Merchant_Payment_Method_Instances]
            if request.data['payment_method'] not in payment_methods: return False
        return True
    
class MerchantStorePermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj):
        store_pk = str(obj['pk'])
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        Merchant_Store_Instances = MerchantStore.objects.filter(merchant_id=Merchant_Instance.id)
        merchant_store_pks = [str(ms.id) for ms in Merchant_Store_Instances]
        
        if request.method == 'PUT':  
            if not MerchantStore.objects.filter(pk=obj['pk']).exists():
                return False 

            if store_pk not in merchant_store_pks:
                return False

        return True
    
class MerchantStoreLogoPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj):
        store_pk = str(obj['store_pk'])
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        Merchant_Store_Instances = MerchantStore.objects.filter(merchant_id=Merchant_Instance.id)
        merchant_store_pks = [str(ms.id) for ms in Merchant_Store_Instances]

        if request.method == 'POST':
            if not MerchantStore.objects.filter(pk=store_pk).exists():
                return False 

            if store_pk not in merchant_store_pks:
                return False

        return True

class MerchantStoreBannerPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj):
        store_pk = str(obj['store_pk'])
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        Merchant_Store_Instances = MerchantStore.objects.filter(merchant_id=Merchant_Instance.id)
        merchant_store_pks = [str(ms.id) for ms in Merchant_Store_Instances]

        if request.method == 'POST':
            if not MerchantStore.objects.filter(pk=store_pk).exists():
                return False 

            if store_pk not in merchant_store_pks:
                return False

        return True

class MerchantStoreCategoryPermission(BasePermission):
    
    message = "Access Denied!"

    def has_permission(self, request, view) -> bool:
        return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj):
        store_pk = str(obj['store_pk'])
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        Merchant_Store_Instances = MerchantStore.objects.filter(merchant_id=Merchant_Instance.id)
        merchant_store_pks = [str(ms.id) for ms in Merchant_Store_Instances]

        if request.method == 'POST':
            if 'merchant_store' not in request.data:
                return False
            
            if not MerchantStore.objects.filter(pk=store_pk).exists():
                return False 

            if store_pk not in merchant_store_pks:
                return False

        return True