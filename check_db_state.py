#!/usr/bin/env python3
"""
データベース状態確認スクリプト

Daily DishのDB状態を詳細に表示します
"""

import os
import sys
import django
from decimal import Decimal

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_dish_project.settings')
django.setup()

from daily_dish.models import User, Recipe, RegisteredRecipe, CookedDish, IngredientCache, ApiKey

def print_separator(title):
    """セパレータ印刷"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def show_users():
    """ユーザー一覧表示"""
    print_separator("USERS テーブル")
    users = User.objects.all().order_by('id')
    
    if not users:
        print("データなし")
        return
    
    print(f"総件数: {users.count()}")
    print()
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Active: {user.is_active}")
        print(f"  Created: {user.created_at}")
        print(f"  Updated: {user.updated_at}")
        print()

def show_recipes():
    """レシピ一覧表示"""
    print_separator("RECIPES テーブル")
    recipes = Recipe.objects.all().order_by('id')
    
    if not recipes:
        print("データなし")
        return
    
    print(f"総件数: {recipes.count()}")
    print()
    
    for recipe in recipes:
        print(f"ID: {recipe.id}")
        print(f"  User: {recipe.user.username} (ID: {recipe.user.id})")
        print(f"  Recipe Name: {recipe.recipe_name}")
        print(f"  Created: {recipe.created_at}")
        
        # 材料表示
        ingredients = recipe.get_ingredients()
        print(f"  Materials ({len(ingredients)} items):")
        for i, ingredient in enumerate(ingredients, 1):
            print(f"    {i}. {ingredient['name']}: {ingredient['amount']}{ingredient['unit']}")
        
        # NULL以外の材料フィールド表示
        print(f"  Raw Fields:")
        for i in range(1, 21):
            ingredient_name = getattr(recipe, f'ingredient_{i}')
            amount = getattr(recipe, f'amount_{i}')
            unit = getattr(recipe, f'unit_{i}')
            
            if ingredient_name:
                print(f"    ingredient_{i}: {ingredient_name}, amount_{i}: {amount}, unit_{i}: {unit}")
        print()

def show_registered_recipes():
    """登録済みレシピ一覧表示"""
    print_separator("REGISTERED_RECIPES テーブル")
    registered = RegisteredRecipe.objects.all().order_by('id')
    
    if not registered:
        print("データなし")
        return
    
    print(f"総件数: {registered.count()}")
    print()
    
    for reg in registered:
        print(f"ID: {reg.id}")
        print(f"  User: {reg.user.username} (ID: {reg.user.id})")
        print(f"  Recipe Name: {reg.recipe_name}")
        print(f"  Type: {reg.recipe_type}")
        
        if reg.recipe_type == 'existing':
            print(f"  URL: {reg.recipe_url}")
            print(f"  Recipe ID: {reg.recipe}")
        else:  # new
            print(f"  URL: {reg.recipe_url}")
            print(f"  Recipe ID: {reg.recipe.id if reg.recipe else None}")
            if reg.recipe:
                print(f"  Related Recipe: {reg.recipe.recipe_name}")
        
        print(f"  Created: {reg.created_at}")
        print()

def show_cooked_dishes():
    """料理履歴一覧表示"""
    print_separator("COOKED_DISHES テーブル")
    cooked = CookedDish.objects.all().order_by('id')
    
    if not cooked:
        print("データなし")
        return
    
    print(f"総件数: {cooked.count()}")
    print()
    
    for dish in cooked:
        print(f"ID: {dish.id}")
        print(f"  User: {dish.user.username} (ID: {dish.user.id})")
        print(f"  Registered Recipe: {dish.registered_recipe.recipe_name} (ID: {dish.registered_recipe.id})")
        print(f"  Created: {dish.created_at}")
        print()

def show_ingredient_cache():
    """食材キャッシュ一覧表示"""
    print_separator("INGREDIENT_CACHE テーブル")
    cache = IngredientCache.objects.all().order_by('user_id', 'ingredient_name')
    
    if not cache:
        print("データなし")
        return
    
    print(f"総件数: {cache.count()}")
    print()
    
    current_user = None
    for item in cache:
        if current_user != item.user:
            current_user = item.user
            print(f"User: {item.user.username} (ID: {item.user.id})")
        
        print(f"  ID: {item.id}")
        print(f"    Ingredient: {item.ingredient_name}")
        print(f"    Amount: {item.amount}")
        print(f"    Unit: {item.unit}")
        print(f"    Created: {item.created_at}")

def show_api_keys():
    """API Key一覧表示"""
    print_separator("API_KEYS テーブル")
    api_keys = ApiKey.objects.all().order_by('id')
    
    if not api_keys:
        print("データなし")
        return
    
    print(f"総件数: {api_keys.count()}")
    print()
    
    for key in api_keys:
        print(f"ID: {key.id}")
        print(f"  Key Name: {key.key_name}")
        print(f"  API Key: {key.api_key}")
        print(f"  Active: {key.is_active}")
        print(f"  Usage Count: {key.usage_count}")
        print(f"  Created: {key.created_at}")
        print(f"  Last Used: {key.last_used_at}")
        print(f"  Expires: {key.expires_at}")
        print()

def show_summary():
    """サマリー表示"""
    print_separator("データベース サマリー")
    
    summary = {
        "Users": User.objects.count(),
        "Recipes": Recipe.objects.count(), 
        "Registered Recipes": RegisteredRecipe.objects.count(),
        "Cooked Dishes": CookedDish.objects.count(),
        "Ingredient Cache": IngredientCache.objects.count(),
        "API Keys": ApiKey.objects.count()
    }
    
    for table, count in summary.items():
        print(f"{table:20}: {count:3d} records")

def main():
    """メイン実行"""
    print("Daily Dish データベース状態確認")
    print(f"実行日時: {django.utils.timezone.now()}")
    
    show_summary()
    show_users()
    show_recipes()
    show_registered_recipes()
    show_cooked_dishes()
    show_ingredient_cache()
    show_api_keys()
    
    print(f"\n{'='*60}")
    print("確認完了")

if __name__ == "__main__":
    main()