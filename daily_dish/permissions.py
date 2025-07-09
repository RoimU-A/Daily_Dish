from rest_framework.permissions import BasePermission
from .models import ApiKey


class IsApiKeyAuthenticated(BasePermission):
    """API Key認証用のパーミッション"""
    
    def has_permission(self, request, view):
        """
        API Key認証が成功している場合のみアクセス許可
        """
        # API Key認証の場合、request.authがApiKeyオブジェクトになる
        return isinstance(request.auth, ApiKey)


class IsJWTAuthenticated(BasePermission):
    """JWT認証用のパーミッション"""
    
    def has_permission(self, request, view):
        """
        JWT認証が成功している場合のみアクセス許可
        """
        # JWT認証の場合、request.userが認証済みユーザーでrequest.authがTokenオブジェクト
        return (request.user and 
                request.user.is_authenticated and 
                hasattr(request, 'auth') and 
                not isinstance(request.auth, ApiKey))


class IsOwnerOrReadOnly(BasePermission):
    """
    オブジェクトの所有者のみが編集可能
    読み取りは認証済みユーザー全員に許可
    """
    
    def has_object_permission(self, request, view, obj):
        # 読み取り権限は認証済みユーザー全員に許可
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # 書き込み権限は所有者のみ
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsOwner(BasePermission):
    """所有者のみアクセス可能"""
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False