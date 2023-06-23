from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from merchants.models import *
from merchants.serializers import *
from merchants.permissions import *

class MCMerchantViewSet(viewsets.ViewSet):
    
    lookup_field = "uid"
    
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
    
    def retrieve(self, request, uid=None):
        self.check_object_permissions(request=request, obj={ 'uid': uid })
        Merchant_Instance = Merchant.objects.get(uid=uid)
        Merchant_Serializer = MerchantSerializer(Merchant_Instance)
        data = Merchant_Serializer.data
        return Response(data, status=status.HTTP_200_OK)

class MCMerchantPaymentMethodViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantPaymentMethodPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Merchant_Payment_Method_Serializer = CreateMerchantPaymentMethodSerializer(data=request.data, context={'request': request})
        if not Create_Merchant_Payment_Method_Serializer.is_valid():
            print(Create_Merchant_Payment_Method_Serializer.errors)           
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        # self.check_object_permissions(request=request, obj={ 'pk': pk })
        # Merchant_Instance = Merchant.objects.get(pk=pk)
        # Merchant_Serializer = MerchantSerializer(Merchant_Instance)
        # data = Merchant_Serializer.data
        return Response(None, status=status.HTTP_200_OK)
    
class MCMerchantSubcriptionViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantSubscriptionPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        return Response(None, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': str(pk)})
        print('retrieve')
        return Response(None, status=status.HTTP_200_OK)