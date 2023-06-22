from rest_framework.permissions import BasePermission
from users.models import User, UserProfile
from users.serializers import UserSerializer

class UserPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        pk = str(obj['user_pk'])
        if str(request.user.id) != pk:
            return False    
        return True

class UserProfilePermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        SAFE_METHODS = ('POST', 'PUT', 'DELETE')
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        User_Serializer = UserSerializer(request.user)
        profile_pk = str(obj['profile_pk'])
        
        if request.method == 'DELETE':
            User_Profile_Instances = UserProfile.objects.filter(pk__in=User_Serializer.data['profiles']).filter(is_account_holder=False)
            user_profile_pks = (str(upi.id) for upi in User_Profile_Instances)
            
            if str(profile_pk) not in user_profile_pks:
                return False
            return True
            
        user_profile_pks = (str(profile) for profile in User_Serializer.data['profiles']) 
        if profile_pk not in user_profile_pks:
            return False
        return True

class UserProfileImagePermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        User_Serializer = UserSerializer(request.user) 
        user_profile_pks = (str(profile) for profile in User_Serializer.data['profiles'])  
        
        if str(request.data['user_profile']) not in user_profile_pks:
            return False
        
        return True

class UserAddressPermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        SAFE_METHODS = ('POST', 'PUT', 'DELETE')
        if request.method in SAFE_METHODS:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        User_Serializer = UserSerializer(request.user) 
        user_address_pks = (str(address) for address in User_Serializer.data['addresses'])

        if str(obj['address_pk']) not in user_address_pks:
            return False

        return True