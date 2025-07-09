from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import get_user_model
from .models import Recipe, CookedDish, IngredientCache
from .serializers import (
    ExternalRecipeSerializer, 
    ExternalCookedDishSerializer, 
    ExternalIngredientCacheSerializer
)
from .permissions import IsApiKeyAuthenticated
from .authentication import ApiKeyAuthentication

User = get_user_model()


class ExternalRecipeListView(generics.ListAPIView):
    """
    外部アプリ向けレシピ一覧API
    GET /api/external/recipes/
    """
    serializer_class = ExternalRecipeSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]
    
    def get_queryset(self):
        # 全ユーザーのレシピを取得（外部アプリは全データアクセス可能）
        return Recipe.objects.all().order_by('-created_at')


class ExternalRecipeDetailView(generics.RetrieveAPIView):
    """
    外部アプリ向けレシピ詳細API
    GET /api/external/recipes/{id}/
    """
    queryset = Recipe.objects.all()
    serializer_class = ExternalRecipeSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]


class ExternalCookedDishListView(generics.ListAPIView):
    """
    外部アプリ向け料理履歴一覧API
    GET /api/external/cooked-dishes/
    """
    serializer_class = ExternalCookedDishSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]
    
    def get_queryset(self):
        return CookedDish.objects.all().order_by('-created_at')


class ExternalCookedDishDetailView(generics.RetrieveAPIView):
    """
    外部アプリ向け料理履歴詳細API
    GET /api/external/cooked-dishes/{id}/
    """
    queryset = CookedDish.objects.all()
    serializer_class = ExternalCookedDishSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]


class ExternalIngredientCacheListView(generics.ListAPIView):
    """
    外部アプリ向け食材キャッシュ一覧API
    GET /api/external/ingredient-cache/
    """
    serializer_class = ExternalIngredientCacheSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]
    
    def get_queryset(self):
        return IngredientCache.objects.all().order_by('-created_at')


class ExternalIngredientCacheDetailView(generics.RetrieveAPIView):
    """
    外部アプリ向け食材キャッシュ詳細API
    GET /api/external/ingredient-cache/{id}/
    """
    queryset = IngredientCache.objects.all()
    serializer_class = ExternalIngredientCacheSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsApiKeyAuthenticated]


@api_view(['GET'])
@authentication_classes([ApiKeyAuthentication])
@permission_classes([IsApiKeyAuthenticated])
def external_stats_view(request):
    """
    外部アプリ向け統計情報API
    GET /api/external/stats/
    """
    stats = {
        'total_recipes': Recipe.objects.count(),
        'total_cooked_dishes': CookedDish.objects.count(),
        'total_users': User.objects.count(),
        'total_ingredient_cache': IngredientCache.objects.count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@authentication_classes([ApiKeyAuthentication])
@permission_classes([IsApiKeyAuthenticated])
def external_recent_activities_view(request):
    """
    外部アプリ向け最近のアクティビティAPI
    GET /api/external/recent-activities/
    """
    # 最近の料理履歴（10件）
    recent_cooked = CookedDish.objects.select_related('recipe').order_by('-created_at')[:10]
    recent_cooked_data = ExternalCookedDishSerializer(recent_cooked, many=True).data
    
    # 最近のレシピ（10件）
    recent_recipes = Recipe.objects.order_by('-created_at')[:10]
    recent_recipes_data = ExternalRecipeSerializer(recent_recipes, many=True).data
    
    activities = {
        'recent_cooked_dishes': recent_cooked_data,
        'recent_recipes': recent_recipes_data,
    }
    
    return Response(activities)