from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from merchants.models import *
from merchants.serializers import *
from merchants.permissions import *
from merchants.ecosystem.methods import *
from pprint import pprint

class MCMerchantViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Merchant_Serializer = CreateMerchantSerializer(data=request.data, context={'request': request, 'user': request.user })
        if not Create_Merchant_Serializer.is_valid():
            return Response(Create_Merchant_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        merchant_data = Create_Merchant_Serializer.validated_data['merchant']
        Merchant_Serializer = MerchantSerializer(merchant_data)
        data = Merchant_Serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={ 'pk': pk })
        Merchant_Instance = Merchant.objects.get(pk=pk)
        Merchant_Serializer = MerchantSerializer(Merchant_Instance)
        data = Merchant_Serializer.data
        return Response(data, status=status.HTTP_200_OK)

class MCMerchantPaymentMethodViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantPaymentMethodPermission ]
        return [ permission() for permission in permission_classes ]

    def list(self, request):
        setup_intent_res = stripe.SetupIntent.create(
            customer=request.user.stripe_customer_id,
            payment_method_types=["card"],
        )
        return Response(setup_intent_res.client_secret, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})

        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        payment_method_res = stripe.PaymentMethod.retrieve(id=request.data['payment_method_id'])

        data = {
            'merchant': Merchant_Instance.id,
            'stripe_pm_id': payment_method_res.id
        }
        
        Create_Merchant_Payment_Method_Serializer = CreateMerchantPaymentMethodSerializer(data=data)
        if not Create_Merchant_Payment_Method_Serializer.is_valid():
            return Response(Create_Merchant_Payment_Method_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Create_Merchant_Payment_Method_Serializer.save()
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': pk})
        Merchant_Payment_Method_Instance = MerchantPaymentMethod.objects.get(pk=str(pk))
        Merchant_Payment_Method_Instance.delete()
        stripe.PaymentMethod.detach(Merchant_Payment_Method_Instance.stripe_pm_id)
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class MCMerchantSubcriptionViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantSubscriptionPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})
        Create_Merchant_Subscription_Serializer = CreateMerchantSubscriptionSerializer(
            data={'merchant_plan': request.data['merchant_plan']}, 
            context={'request': request}
        )
        
        if not Create_Merchant_Subscription_Serializer.is_valid():
            return Response(Create_Merchant_Subscription_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = get_merchant_data(Create_Merchant_Subscription_Serializer.validated_data['merchant'])
        return Response(data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': str(pk)})
        print('retrieve')
        return Response(None, status=status.HTTP_200_OK)
    
class MCMerchantPlanViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, pk=None):
        data = get_merchant_plan_data()
        return Response(data, status=status.HTTP_200_OK)  

class MCMerchantStoreViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated, MerchantStorePermission]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        Create_Merchant_Store_Serializer = CreateMerchantStoreSerializer(data=request.data, context={'request': request})
        if not Create_Merchant_Store_Serializer.is_valid():
            return Response(Create_Merchant_Store_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        Merchant_Instance = Create_Merchant_Store_Serializer.validated_data['merchant']
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)  
    
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': pk})
        Merchant_Store_Instance = MerchantStore.objects.get(pk=pk)
        Edit_Merchant_Store_Serializer = EditMerchantStoreSerializer(Merchant_Store_Instance, data=request.data)
        
        if not Edit_Merchant_Store_Serializer.is_valid():
            return Response(Edit_Merchant_Store_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_Merchant_Store_Serializer.save()
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_202_ACCEPTED)  
    
class MCMerchantStoreLogoViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated, MerchantStoreLogoPermission]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        self.check_object_permissions(request=request, obj={'store_pk': request.data['merchant_store']})
        is_merchant_store_logo = MerchantStoreLogo.objects.filter(merchant_store_id=str(request.data['merchant_store'])).exists()
        if is_merchant_store_logo:
            Merchant_Store_Logo_Instance = MerchantStoreLogo.objects.get(merchant_store_id=str(request.data['merchant_store']))
            # remove image from cdn maybe??? idk yet
            Merchant_Store_Logo_Instance.delete()
        
        Create_Merchant_Store_Logo_Serializer = CreateMerchantStoreLogoSerializer(data=request.data, context={ 'request': request })
        if not Create_Merchant_Store_Logo_Serializer.is_valid():
            return Response(Create_Merchant_Store_Logo_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)

class MCMerchantStoreBannerViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated, MerchantStoreBannerPermission]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        self.check_object_permissions(request=request, obj={'store_pk': request.data['merchant_store']})
        is_merchant_store_banner = MerchantStoreLogo.objects.filter(merchant_store_id=str(request.data['merchant_store'])).exists()
        if is_merchant_store_banner:
            Merchant_Store_Banner_Instance = MerchantStoreBanner.objects.get(merchant_store_id=str(request.data['merchant_store']))
            # remove image from cdn maybe??? idk yet
            Merchant_Store_Banner_Instance.delete()
        
        Create_Merchant_Store_Banner_Serializer = CreateMerchantStoreBannerSerializer(data=request.data, context={ 'request': request })
        if not Create_Merchant_Store_Banner_Serializer.is_valid():
            return Response(Create_Merchant_Store_Banner_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)

class MCMerchantStoreCategoryViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated, MerchantStoreCategoryPermission]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        self.check_object_permissions(request=request, obj={'store_pk': request.data['merchant_store']})
        Merchant_Store_Category_Serializer = MerchantStoreCategorySerializer(data=request.data)
        
        if not Merchant_Store_Category_Serializer.is_valid():
            return Response(Merchant_Store_Category_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Merchant_Store_Category_Serializer.save()
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id)) 
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        # self.check_object_permissions(request=request, obj={'store_pk': request.data['merchant_store']})
        
        return Response(None, status=status.HTTP_201_CREATED)