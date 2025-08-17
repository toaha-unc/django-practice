from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """
    Custom permission to only allow librarians to perform actions.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated and is a staff member (librarian)
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsMember(permissions.BasePermission):
    """
    Custom permission to only allow members to perform certain actions.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated (member)
        return request.user and request.user.is_authenticated


class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow librarians full access and members read-only access.
    """
    
    def has_permission(self, request, view):
        # Allow read operations for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Allow write operations only for librarians
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsLibrarianOrMemberReadOnly(permissions.BasePermission):
    """
    Custom permission to allow librarians full access and members read-only access to borrowing operations.
    """
    
    def has_permission(self, request, view):
        # Allow read operations for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Allow write operations for librarians and borrowing/returning for members
        if request.user and request.user.is_authenticated:
            # Allow borrowing and returning operations for all authenticated users
            if view.action in ['borrow', 'return_book']:
                return True
            # Allow other write operations only for librarians
            return request.user.is_staff
        
        return False
