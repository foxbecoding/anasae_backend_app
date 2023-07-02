from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import *
from users.models import UserProfile, UserProfileImage
from users.permissions import *
from users.ecosystem.methods import Prepare_User_Data
import os, requests

class MPAUserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserPermission]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'user_pk': pk})
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_200_OK)
        
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'user_pk': pk})
        User_Instance = request.user
        Edit_User_Serializer = EditUserSerializer(User_Instance, data=request.data)
        
        if not Edit_User_Serializer.is_valid():
            return Response(Edit_User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_User_Serializer.save()
        data = Prepare_User_Data(User_Instance)
        return Response(data, status=status.HTTP_202_ACCEPTED)      

class MPAUserProfileViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserProfilePermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_User_Profile_Serializer = CreateUserProfileSerializer(data=request.data, context={'user': request.user})
        
        if not Create_User_Profile_Serializer.is_valid(): 
            return Response(Create_User_Profile_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
        
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'profile_pk': pk})
        User_Profile_Instance = UserProfile.objects.get(pk=pk)
        Edit_User_Profile_Serializer = EditUserProfileSerializer(User_Profile_Instance, data=request.data)
        
        if not Edit_User_Profile_Serializer.is_valid():
            return Response(Edit_User_Profile_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_User_Profile_Serializer.save()
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
        
          
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'profile_pk': pk})
        User_Profile_Instance = UserProfile.objects.get(pk=pk)
        User_Profile_Instance.delete()
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class MPAUserProfileImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserProfileImagePermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        is_User_Profile_Image = UserProfileImage.objects.filter(user_profile_id=str(request.data['user_profile'])).exists()
        if is_User_Profile_Image:
            User_Profile_Image = UserProfileImage.objects.get(user_profile_id=str(request.data['user_profile']))
            # os.remove(os.getenv('MEDIA_ROOT')+str(User_Profile_Image.image))
            User_Profile_Image.delete()
        
        Create_User_Profile_Image_Serializer = CreateUserProfileImageSerializer(data=request.data, context={ 'request': request })
        if not Create_User_Profile_Image_Serializer.is_valid():
            return Response(Create_User_Profile_Image_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
           
class MPAUserAddressViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserAddressPermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_User_Address_Serializer = CreateUserAddressSerializer(
            data=request.data, 
            context={'user': request.user}
        )

        if not Create_User_Address_Serializer.is_valid():
            return Response(Create_User_Address_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
          
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'address_pk': pk})
        User_Address_Instance = UserAddress.objects.get(pk=pk)
        Edit_User_Address_Serializer = EditUserAddressSerializer(User_Address_Instance, data=request.data)

        if not Edit_User_Address_Serializer.is_valid():
            return Response(Edit_User_Address_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_User_Address_Serializer.save()
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
        
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'address_pk': pk})
        User_Address_Instance = UserAddress.objects.get(pk=pk)
        User_Address_Instance.delete()
        data = Prepare_User_Data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)