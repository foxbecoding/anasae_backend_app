from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import *
from users.models import UserProfile
from users.ecosystem.methods import Prepare_User_Data
from utils.helpers import is_valid_square_img

class MPAUserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        if str(pk) == str(request.user.id):
            data = Prepare_User_Data(request.user)
            return Response(data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        if str(pk) == str(request.user.id):
            User_Instance = request.user
            Edit_User_Serializer = EditUserSerializer(User_Instance, data=request.data)
            if Edit_User_Serializer.is_valid():
                Edit_User_Serializer.save()
                data = Prepare_User_Data(User_Instance)
                return Response(data, status=status.HTTP_202_ACCEPTED)
            return Response(Edit_User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)

class MPAUserProfileViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        request_data = {
            'user': str(request.user.id),
            'name': request.data['name']
        }
        
        User_Profile_Serializer = UserProfileSerializer(data=request_data)
        if User_Profile_Serializer.is_valid(): 
            User_Profile_Serializer.save()
            data = Prepare_User_Data(request.user)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(User_Profile_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        User_Serializer = UserSerializer(request.user) 
        user_profile_pks = [ str(profile) for profile in User_Serializer.data['profiles'] ] 
        if str(pk) in user_profile_pks:
            User_Profile_Instance = UserProfile.objects.get(pk=pk)
            Edit_User_Profile_Serializer = EditUserProfileSerializer(User_Profile_Instance, data=request.data)
            if Edit_User_Profile_Serializer.is_valid():
                Edit_User_Profile_Serializer.save()
                data = Prepare_User_Data(request.user)
                return Response(data, status=status.HTTP_202_ACCEPTED)
            return Response(Edit_User_Profile_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
    
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        User_Serializer = UserSerializer(request.user) 
        User_Profile_Instances = UserProfile.objects.filter(pk__in=User_Serializer.data['profiles']).filter(is_account_holder=False)
        user_profile_pks = [ str(upi.id) for upi in User_Profile_Instances ]  
        if str(pk) in user_profile_pks:
            User_Profile_Instance = UserProfile.objects.get(pk=pk)
            User_Profile_Instance.delete()
            data = Prepare_User_Data(request.user)
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
    
class MPAUserProfileImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        User_Serializer = UserSerializer(request.user) 
        user_profile_pks = [ str(profile) for profile in User_Serializer.data['profiles'] ]  
        if str(request.data['user_profile']) in user_profile_pks:
            Create_User_Profile_Image_Serializer = CreateUserProfileImageSerializer(data=request.data, context={ 'request': request })
            if Create_User_Profile_Image_Serializer.is_valid():
                data = Prepare_User_Data(request.user)
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(Create_User_Profile_Image_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)