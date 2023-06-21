from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from merchants.models import *
from merchants.serializers import *

class MCMerchantViewSet(viewsets.ViewSet):
    lookup_field = "uid"
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Merchant_Serializer = CreateMerchantSerializer(data=request.data, context={'request': request, 'user': request.user })
        if Create_Merchant_Serializer.is_valid():
            merchant_data = Create_Merchant_Serializer.validated_data['merchant']
            Merchant_Serializer = MerchantSerializer(merchant_data)
            data = Merchant_Serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(Create_Merchant_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(csrf_protect)
    def retrieve(self, request, uid=None):
        return Response(None, status=status.HTTP_200_OK)
    
class MCMerchantSubcriptionViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        return Response(None, status=status.HTTP_200_OK)