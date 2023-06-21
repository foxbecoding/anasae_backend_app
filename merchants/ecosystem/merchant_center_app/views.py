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
        Merchant_Serializer = MerchantSerializer(data=request.data, context={ 'user': request.user })
        if Merchant_Serializer.is_valid():
            Merchant_Serializer.validated_data['merchant']
            return Response(None, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def retrieve(self, request, uid=None):
        return Response(None, status=status.HTTP_200_OK)