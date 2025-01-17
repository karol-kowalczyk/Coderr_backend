from rest_framework import permissions

class IsObjectOwnerOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and (request.user == obj.user or request.user.is_staff)
        
        if request.method == "PATCH":
            return request.user and (request.user == obj.user or request.user.is_staff)

        return request.user and (request.user == obj.user or request.user.is_staff)
    

class IsBusinessOrAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                not request.user.is_staff and
                request.user.user_profile.type == 'business'
            )
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                request.user.is_authenticated and 
                (request.user.is_staff or request.user.user_profile.type == 'business')
            )
                    
        return False
    

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff or request.user.user_profile.type == 'business'
        
        return False
        
