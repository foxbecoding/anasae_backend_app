from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import UserLogin
from users.serializers import UserSerializer, UserSignUpSerializer, UserLoginSerializer


class AccountSignUpViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = UserSignUpSerializer(data=request.data, context={ 'request': request })
        if serializer.is_valid():
            user = serializer.validated_data['user']
            #login user
            # login(request, user)
            user_serialized = UserSerializer(user)
            return Response(user_serialized.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountLogInViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = UserLoginSerializer(data=request.data, context={ 'request': request })
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            UserLogin.objects.create(user = user).save()
            user_serialized = UserSerializer(user)
            response = Response(user_serialized.data, status=status.HTTP_202_ACCEPTED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response 
    
class AccountLogOutViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK) 