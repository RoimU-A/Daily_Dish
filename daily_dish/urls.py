from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views_web, views_external, views_line

app_name = 'daily_dish'

# Web API用のURL設定
web_patterns = [
    # 認証関連
    path('auth/login/', TokenObtainPairView.as_view(), name='web_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='web_refresh'),
    path('auth/register/', views_web.UserCreateView.as_view(), name='web_register'),
    path('auth/profile/', views_web.UserProfileView.as_view(), name='web_profile'),
    
    # レシピ管理
    path('recipes/', views_web.RecipeListCreateView.as_view(), name='web_recipe_list'),
    path('recipes/<int:pk>/', views_web.RecipeDetailView.as_view(), name='web_recipe_detail'),
    
    # 料理履歴管理
    path('cooked-dishes/', views_web.CookedDishListCreateView.as_view(), name='web_cooked_dish_list'),
    path('cooked-dishes/<int:pk>/', views_web.CookedDishDetailView.as_view(), name='web_cooked_dish_detail'),
    
    # 食材キャッシュ管理
    path('ingredient-cache/', views_web.IngredientCacheListCreateView.as_view(), name='web_ingredient_cache_list'),
    path('ingredient-cache/<int:pk>/', views_web.IngredientCacheDetailView.as_view(), name='web_ingredient_cache_detail'),
    path('ingredient-cache/bulk-delete/', views_web.ingredient_cache_bulk_delete_view, name='web_ingredient_cache_bulk_delete'),
    
    # 統計・分析
    path('stats/', views_web.user_stats_view, name='web_stats'),
    path('recent-activities/', views_web.user_recent_activities_view, name='web_recent_activities'),
    path('dashboard/', views_web.user_dashboard_view, name='web_dashboard'),
]

# 外部API用のURL設定
external_patterns = [
    # レシピ情報（読み取り専用）
    path('recipes/', views_external.ExternalRecipeListView.as_view(), name='external_recipe_list'),
    path('recipes/<int:pk>/', views_external.ExternalRecipeDetailView.as_view(), name='external_recipe_detail'),
    
    # 料理履歴情報（読み取り専用）
    path('cooked-dishes/', views_external.ExternalCookedDishListView.as_view(), name='external_cooked_dish_list'),
    path('cooked-dishes/<int:pk>/', views_external.ExternalCookedDishDetailView.as_view(), name='external_cooked_dish_detail'),
    
    # 食材キャッシュ情報（読み取り専用）
    path('ingredient-cache/', views_external.ExternalIngredientCacheListView.as_view(), name='external_ingredient_cache_list'),
    path('ingredient-cache/<int:pk>/', views_external.ExternalIngredientCacheDetailView.as_view(), name='external_ingredient_cache_detail'),
    
    # 統計・分析情報
    path('stats/', views_external.external_stats_view, name='external_stats'),
    path('recent-activities/', views_external.external_recent_activities_view, name='external_recent_activities'),
    
    # LINE連携機能
    path('users/link-line/', views_line.link_line_user, name='link_line_user'),
    path('recipes/from-line/', views_line.register_recipe_from_line, name='register_recipe_from_line'),
    path('line/webhook/', views_line.line_webhook, name='line_webhook'),
]

# メインのURL設定
urlpatterns = [
    path('api/web/', include(web_patterns)),
    path('api/external/', include(external_patterns)),
]