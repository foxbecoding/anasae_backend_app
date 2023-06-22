from rest_framework.permissions import BasePermission
from users.models import User
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
        SAFE_METHODS = ['POST', 'PUT', 'DELETE']
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        User_Serializer = UserSerializer(request.user) 
        user_profile_pks = [str(profile) for profile in User_Serializer.data['profiles']] 
        if str(obj['profile_pk']) not in user_profile_pks:
            return False
        return True