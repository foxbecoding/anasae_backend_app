from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import *


class AccountSignUpViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        User_Sign_Up_Serializer = UserSignUpSerializer(data=request.data, context={ 'request': request })
        if User_Sign_Up_Serializer.is_valid():
            user = User_Sign_Up_Serializer.validated_data['user']
            #login user
            # login(request, user)
            
            #Set user Gender
            user_gender_data = {
                'user_gender': request.data['gender'], 
                'user': user.id
            }
            
            User_Gender_Choice_Serializer = UserGenderChoiceSerializer(data=user_gender_data)
            if User_Gender_Choice_Serializer.is_valid(): User_Gender_Choice_Serializer.save()
            
            #Create user profile
            user_profile_data = {
                'user': user.id,
                'name': user.first_name+' '+user.last_name[0],
                'is_account_holder': True
            }

            User_Profile_Serializer = UserProfileSerializer(data=user_profile_data)
            if User_Profile_Serializer.is_valid(): User_Profile_Serializer.save()

            User_Serializer = UserSerializer(user)
            return Response(User_Serializer.data, status=status.HTTP_201_CREATED)
        return Response(User_Sign_Up_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountLogInViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        User_Login_Serializer = AccountLoginSerializer(data=request.data, context={ 'request': request })
        if User_Login_Serializer.is_valid():
            user = User_Login_Serializer.validated_data['user']
            login(request, user)
            
            User_Account_Login_Serializer = UserLoginSerializer(data={'user': user.id})
            if User_Account_Login_Serializer.is_valid(): User_Account_Login_Serializer.save()
            
            User_Serializer = UserSerializer(user)
            response = Response(User_Serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            response = Response(User_Login_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response 
    
class AccountLogOutViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK) 