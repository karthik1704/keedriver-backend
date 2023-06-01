from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """
    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user 
    

class IsDriver(BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """
    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        print(obj.driver)
        return obj.driver == request.user 