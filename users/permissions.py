from rest_framework.permissions import BasePermission
from users.models import User

class UserPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        pk = str(obj['pk'])
        
        # if not User.objects

        if str(request.user.id) != pk:
            return False
        
        return True