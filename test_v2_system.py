#!/usr/bin/env python3
"""
Daily Dish v2 システム統合テスト
統一されたレシピ管理システムのテスト
"""

import requests
import json
import time

# 設定
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser_v2",
    "password": "testpassword123"
}
API_KEY = "test-api-key-v2-12345"

def test_jwt_login():
    """JWT認証テスト"""
    print("=== JWT認証テスト ===")
    
    url = f"{BASE_URL}/api/web/auth/login/"
    response = requests.post(url, json=TEST_USER)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ JWT認証成功: {data['access'][:50]}...")
        return data['access']
    else:
        print(f"❌ JWT認証失敗: {response.status_code}")
        print(response.text)
        return None

def test_recipe_creation(access_token):
    """統一レシピ作成テスト"""
    print("\n=== 統一レシピ作成テスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 既存レシピのテスト
    print("1. 既存レシピ作成テスト")
    existing_recipe = {
        "recipe_name": "クックパッドのカレーライス",
        "recipe_url": "https://cookpad.com/recipe/12345",
        "ingredient_1": "牛肉", "amount_1": 300.0, "unit_1": "g",
        "ingredient_2": "じゃがいも", "amount_2": 2.0, "unit_2": "個",
        "ingredient_3": "人参", "amount_3": 1.0, "unit_3": "本"
    }
    
    url = f"{BASE_URL}/api/web/recipes/"
    response = requests.post(url, json=existing_recipe, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 既存レシピ作成成功: {data['recipe_name']}")
        print(f"   URL: {data['recipe_url']}")
        print(f"   材料数: {len(data['ingredients'])}")
        print(f"   既存レシピ判定: {data['is_existing_recipe']}")
        existing_recipe_id = data['id']
    else:
        print(f"❌ 既存レシピ作成失敗: {response.status_code}")
        print(response.text)
        existing_recipe_id = None
    
    # 新規レシピのテスト
    print("\n2. 新規レシピ作成テスト")
    new_recipe = {
        "recipe_name": "手作りハンバーグ",
        "ingredient_1": "牛ひき肉", "amount_1": 400.0, "unit_1": "g",
        "ingredient_2": "玉ねぎ", "amount_2": 1.0, "unit_2": "個",
        "ingredient_3": "パン粉", "amount_3": 50.0, "unit_3": "g"
    }
    
    response = requests.post(url, json=new_recipe, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 新規レシピ作成成功: {data['recipe_name']}")
        print(f"   URL: {data['recipe_url']}")  # None should be displayed
        print(f"   材料数: {len(data['ingredients'])}")
        print(f"   新規レシピ判定: {data['is_new_recipe']}")
        new_recipe_id = data['id']
    else:
        print(f"❌ 新規レシピ作成失敗: {response.status_code}")
        print(response.text)
        new_recipe_id = None
    
    return existing_recipe_id, new_recipe_id

def test_recipe_list(access_token):
    """レシピ一覧取得テスト"""
    print("\n=== レシピ一覧取得テスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{BASE_URL}/api/web/recipes/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ レシピ一覧取得成功: {data['count']}件")
        for recipe in data['results'][:3]:  # 最初の3件を表示
            print(f"   - {recipe['recipe_name']} (URL: {recipe.get('recipe_url', 'None')})")
    else:
        print(f"❌ レシピ一覧取得失敗: {response.status_code}")
        print(response.text)

def test_cooked_dish_creation(access_token, recipe_id):
    """料理履歴作成テスト（v2簡略化版）"""
    print("\n=== 料理履歴作成テスト ===")
    
    if not recipe_id:
        print("❌ レシピIDがないため、料理履歴テストをスキップ")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{BASE_URL}/api/web/cooked-dishes/"
    
    cooked_dish = {"recipe": recipe_id}
    
    response = requests.post(url, json=cooked_dish, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 料理履歴作成成功")
        print(f"   レシピ名: {data['recipe_detail']['recipe_name']}")
        print(f"   料理日時: {data['created_at']}")
        return data['id']
    else:
        print(f"❌ 料理履歴作成失敗: {response.status_code}")
        print(response.text)
        return None

def test_cooked_dish_list(access_token):
    """料理履歴一覧取得テスト"""
    print("\n=== 料理履歴一覧取得テスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{BASE_URL}/api/web/cooked-dishes/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 料理履歴一覧取得成功: {data['count']}件")
        for dish in data['results']:
            print(f"   - {dish['recipe_detail']['recipe_name']} ({dish['created_at'][:10]})")
    else:
        print(f"❌ 料理履歴一覧取得失敗: {response.status_code}")
        print(response.text)

def test_external_api():
    """外部API（API Key認証）テスト"""
    print("\n=== 外部APIテスト ===")
    
    headers = {"X-API-KEY": API_KEY}
    
    # 統計情報取得
    url = f"{BASE_URL}/api/external/stats/"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 外部統計API成功:")
        print(f"   総レシピ数: {data['total_recipes']}")
        print(f"   総料理履歴数: {data['total_cooked_dishes']}")
        print(f"   総ユーザー数: {data['total_users']}")
    else:
        print(f"❌ 外部統計API失敗: {response.status_code}")
        print(response.text)

def test_user_stats(access_token):
    """ユーザー統計情報テスト"""
    print("\n=== ユーザー統計情報テスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{BASE_URL}/api/web/stats/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ユーザー統計取得成功:")
        print(f"   レシピ数: {data['total_recipes']}")
        print(f"   料理履歴数: {data['total_cooked_dishes']}")
        print(f"   食材キャッシュ数: {data['total_ingredient_cache']}")
    else:
        print(f"❌ ユーザー統計取得失敗: {response.status_code}")
        print(response.text)

def main():
    """メインテスト実行"""
    print("Daily Dish v2 システム統合テスト開始")
    print("=" * 50)
    
    # 1. JWT認証テスト
    access_token = test_jwt_login()
    if not access_token:
        print("認証に失敗したため、テストを中止します")
        return
    
    # 2. 統一レシピ作成テスト
    existing_id, new_id = test_recipe_creation(access_token)
    
    # 3. レシピ一覧テスト
    test_recipe_list(access_token)
    
    # 4. 料理履歴作成テスト
    cooked_id = test_cooked_dish_creation(access_token, existing_id or new_id)
    
    # 5. 料理履歴一覧テスト
    test_cooked_dish_list(access_token)
    
    # 6. ユーザー統計テスト
    test_user_stats(access_token)
    
    # 7. 外部APIテスト
    test_external_api()
    
    print("\n" + "=" * 50)
    print("Daily Dish v2 システム統合テスト完了")

if __name__ == "__main__":
    main()