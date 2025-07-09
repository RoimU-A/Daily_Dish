from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .models import Recipe, CookedDish, IngredientCache
from .serializers import (
    UserSerializer, UserCreateSerializer,
    RecipeSerializer,
    CookedDishSerializer, IngredientCacheSerializer
)
from .permissions import IsJWTAuthenticated, IsOwner, IsOwnerOrReadOnly
from .authentication import HybridAuthentication

User = get_user_model()


# 認証関連
class UserCreateView(generics.CreateAPIView):
    """
    ユーザー登録API
    POST /api/web/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []  # 登録は誰でも可能


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    ユーザープロフィール取得・更新API
    GET/PUT/PATCH /api/web/auth/profile/
    """
    serializer_class = UserSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated]
    
    def get_object(self):
        return self.request.user


# レシピ関連
class RecipeListCreateView(generics.ListCreateAPIView):
    """
    レシピ一覧・作成API
    GET/POST /api/web/recipes/
    """
    serializer_class = RecipeSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated]
    
    def get_queryset(self):
        # ログインユーザーのレシピのみ取得
        return Recipe.objects.filter(user=self.request.user).order_by('-created_at')


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    レシピ詳細・更新・削除API
    GET/PUT/PATCH/DELETE /api/web/recipes/{id}/
    """
    serializer_class = RecipeSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


# 料理履歴関連
class CookedDishListCreateView(generics.ListCreateAPIView):
    """
    料理履歴一覧・作成API
    GET/POST /api/web/cooked-dishes/
    """
    serializer_class = CookedDishSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated]
    
    def get_queryset(self):
        return CookedDish.objects.filter(user=self.request.user).order_by('-created_at')


class CookedDishDetailView(generics.RetrieveDestroyAPIView):
    """
    料理履歴詳細・削除API
    GET/DELETE /api/web/cooked-dishes/{id}/
    """
    serializer_class = CookedDishSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated, IsOwner]
    
    def get_queryset(self):
        return CookedDish.objects.filter(user=self.request.user)


# 食材キャッシュ関連
class IngredientCacheListCreateView(generics.ListCreateAPIView):
    """
    食材キャッシュ一覧・作成API
    GET/POST /api/web/ingredient-cache/
    """
    serializer_class = IngredientCacheSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated]
    
    def get_queryset(self):
        return IngredientCache.objects.filter(user=self.request.user).order_by('-created_at')


class IngredientCacheDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    食材キャッシュ詳細・更新・削除API
    GET/PUT/PATCH/DELETE /api/web/ingredient-cache/{id}/
    """
    serializer_class = IngredientCacheSerializer
    authentication_classes = [HybridAuthentication]
    permission_classes = [IsJWTAuthenticated, IsOwner]
    
    def get_queryset(self):
        return IngredientCache.objects.filter(user=self.request.user)


# 統計・分析関連
@api_view(['GET'])
@authentication_classes([HybridAuthentication])
@permission_classes([IsJWTAuthenticated])
def user_stats_view(request):
    """
    ユーザー統計情報API
    GET /api/web/stats/
    """
    user = request.user
    
    stats = {
        'total_recipes': Recipe.objects.filter(user=user).count(),
        'total_cooked_dishes': CookedDish.objects.filter(user=user).count(),
        'total_ingredient_cache': IngredientCache.objects.filter(user=user).count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@authentication_classes([HybridAuthentication])
@permission_classes([IsJWTAuthenticated])
def user_recent_activities_view(request):
    """
    ユーザーの最近のアクティビティAPI
    GET /api/web/recent-activities/
    """
    user = request.user
    
    # 最近の料理履歴（5件）
    recent_cooked = CookedDish.objects.filter(user=user).select_related('recipe').order_by('-created_at')[:5]
    recent_cooked_data = CookedDishSerializer(recent_cooked, many=True).data
    
    # 最近のレシピ（5件）
    recent_recipes = Recipe.objects.filter(user=user).order_by('-created_at')[:5]
    recent_recipes_data = RecipeSerializer(recent_recipes, many=True).data
    
    activities = {
        'recent_cooked_dishes': recent_cooked_data,
        'recent_recipes': recent_recipes_data,
    }
    
    return Response(activities)


@api_view(['GET'])
@authentication_classes([HybridAuthentication])
@permission_classes([IsJWTAuthenticated])
def user_dashboard_view(request):
    """
    ユーザーダッシュボード情報API
    GET /api/web/dashboard/
    """
    user = request.user
    
    # 統計情報
    stats = {
        'total_recipes': Recipe.objects.filter(user=user).count(),
        'total_cooked_dishes': CookedDish.objects.filter(user=user).count(),
        'total_ingredient_cache': IngredientCache.objects.filter(user=user).count(),
    }
    
    # 最近のアクティビティ
    recent_cooked = CookedDish.objects.filter(user=user).select_related('recipe').order_by('-created_at')[:3]
    recent_cooked_data = CookedDishSerializer(recent_cooked, many=True).data
    
    dashboard = {
        'stats': stats,
        'recent_activities': recent_cooked_data,
        'user_info': UserSerializer(user).data,
    }
    
    return Response(dashboard)