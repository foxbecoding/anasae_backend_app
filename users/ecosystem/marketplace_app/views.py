from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.serializers import *


class MAUserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk=None):
        if User.objects.filter(pk=pk).exists():
            User_Instance = User.objects.get(pk=pk)
            User_Serializer = UserSerializer(User_Instance)
            
            return Response(None, status=status.HTTP_200_OK)