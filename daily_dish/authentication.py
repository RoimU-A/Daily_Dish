from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import ApiKey
from django.utils import timezone

User = get_user_model()


class ApiKeyAuthentication(BaseAuthentication):
    """API Key認証クラス"""
    
    def authenticate(self, request):
        """
        API Keyによる認証を実行
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        try:
            api_key_obj = ApiKey.objects.get(api_key=api_key, is_active=True)
            
            # 有効期限チェック
            if api_key_obj.expires_at and api_key_obj.expires_at < timezone.now():
                raise AuthenticationFailed('API Key has expired')
            
            # 使用回数と最終使用日時を更新
            api_key_obj.usage_count += 1
            api_key_obj.last_used_at = timezone.now()
            api_key_obj.save()
            
            # API Key認証の場合は特別なユーザーオブジェクトを返す
            # 実際の認証には使用しないが、ログ等で識別するため
            return (None, api_key_obj)
            
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')
    
    def authenticate_header(self, request):
        return 'X-API-KEY'


class HybridAuthentication(BaseAuthentication):
    """
    API Key認証とJWT認証のハイブリッド認証
    外部アプリ: API Key
    Webアプリ: JWT
    """
    
    def authenticate(self, request):
        """
        まずAPI Key認証を試し、次にJWT認証を試す
        """
        # API Key認証を試行
        api_key_auth = ApiKeyAuthentication()
        result = api_key_auth.authenticate(request)
        if result:
            return result
        
        # JWT認証を試行
        from rest_framework_simplejwt.authentication import JWTAuthentication
        jwt_auth = JWTAuthentication()
        try:
            return jwt_auth.authenticate(request)
        except:
            return None
    
    def authenticate_header(self, request):
        return 'Bearer or X-API-KEY'