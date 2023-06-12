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
        if str(pk) == str(request.user.id):
            User_Instance = request.user
            User_Serializer = UserSerializer(User_Instance)
            User_Data = User_Serializer.data
            data = prepare_user_data(User_Data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
    @method_decorator(csrf_protect)
    def partial_update(self, request, pk=None):
        if str(pk) == str(request.user.id):
            User_Instance = request.user
            User_Serializer = UserSerializer(User_Instance, data=request.data)
            if User_Serializer.is_valid():
                User_Serializer.save()
                User_Data = User_Serializer.data
                data = prepare_user_data(User_Data)
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else: 
                return Response(User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
def prepare_user_data(User_Data):
    User_Login_Instance = UserLogin.objects.filter(pk__in=User_Data['logins'])
    User_Account_Login_Serializer = UserAccountLoginSerializer(User_Login_Instance, many=True)
    user_logins = []

    for login in User_Account_Login_Serializer.data:
        user_logins.append({
            'pk': login['pk'],
            'logged_in_date': login['created']
        })

    User_Profile_Instance = UserProfile.objects.filter(pk__in=User_Data['profiles'])
    User_Profile_Serializer = UserProfileSerializer(User_Profile_Instance, many=True)
    user_profiles = []

    for profile in User_Profile_Serializer.data:
        user_profiles.append({
            'pk': profile['pk'],
            'name': profile['name'],
            'is_account_holder': profile['is_account_holder'],
        })

    data = {
        'pk': User_Data['pk'],
        'uid': User_Data['uid'],
        'first_name': User_Data['first_name'],
        'last_name': User_Data['last_name'],
        'email': User_Data['email'],
        'logins': user_logins,
        'profiles': user_profiles
    }

    return data