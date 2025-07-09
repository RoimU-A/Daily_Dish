#!/usr/bin/env python3
"""
Daily Dish API テスト用スクリプト

使用方法:
1. Django開発サーバーを起動: python manage.py runserver
2. このスクリプトを実行: python test_api_examples.py

注意: requestsライブラリが必要です
pip install requests
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_registration_and_login():
    """ユーザー登録とログインのテスト"""
    print("=== ユーザー登録とログインのテスト ===")
    
    # 1. ユーザー登録
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/web/auth/register/", json=register_data)
    print(f"ユーザー登録: {response.status_code}")
    if response.status_code == 201:
        print("✅ ユーザー登録成功")
    else:
        print(f"❌ ユーザー登録失敗: {response.text}")
        return None, None
    
    # 2. ログイン
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/web/auth/login/", json=login_data)
    print(f"ログイン: {response.status_code}")
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access"]
        refresh_token = tokens["refresh"]
        print("✅ ログイン成功")
        return access_token, refresh_token
    else:
        print(f"❌ ログイン失敗: {response.text}")
        return None, None

def test_recipe_crud(access_token):
    """レシピCRUDのテスト"""
    print("\n=== レシピCRUDのテスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 1. レシピ作成
    recipe_data = {
        "recipe_name": "親子丼",
        "ingredient_1": "鶏肉",
        "amount_1": "300.0",
        "unit_1": "g",
        "ingredient_2": "玉ねぎ",
        "amount_2": "1.0",
        "unit_2": "個",
        "ingredient_3": "卵",
        "amount_3": "3.0",
        "unit_3": "個"
    }
    
    response = requests.post(f"{BASE_URL}/api/web/recipes/", json=recipe_data, headers=headers)
    print(f"レシピ作成: {response.status_code}")
    if response.status_code == 201:
        recipe = response.json()
        recipe_id = recipe["id"]
        print(f"✅ レシピ作成成功: ID={recipe_id}")
        print(f"   材料数: {len(recipe['ingredients'])}")
    else:
        print(f"❌ レシピ作成失敗: {response.text}")
        return
    
    # 2. レシピ一覧取得
    response = requests.get(f"{BASE_URL}/api/web/recipes/", headers=headers)
    print(f"レシピ一覧取得: {response.status_code}")
    if response.status_code == 200:
        recipes = response.json()
        print(f"✅ レシピ一覧取得成功: {recipes['count']}件")
    else:
        print(f"❌ レシピ一覧取得失敗: {response.text}")
    
    # 3. レシピ詳細取得
    response = requests.get(f"{BASE_URL}/api/web/recipes/{recipe_id}/", headers=headers)
    print(f"レシピ詳細取得: {response.status_code}")
    if response.status_code == 200:
        recipe = response.json()
        print(f"✅ レシピ詳細取得成功: {recipe['recipe_name']}")
    else:
        print(f"❌ レシピ詳細取得失敗: {response.text}")
    
    # 4. レシピ更新
    update_data = {
        "recipe_name": "親子丼（改良版）",
        "ingredient_4": "ご飯",
        "amount_4": "300.0",
        "unit_4": "g"
    }
    
    response = requests.patch(f"{BASE_URL}/api/web/recipes/{recipe_id}/", json=update_data, headers=headers)
    print(f"レシピ更新: {response.status_code}")
    if response.status_code == 200:
        recipe = response.json()
        print(f"✅ レシピ更新成功: {recipe['recipe_name']}")
    else:
        print(f"❌ レシピ更新失敗: {response.text}")
    
    return recipe_id

def test_registered_recipe(access_token, recipe_id):
    """登録済みレシピのテスト"""
    print("\n=== 登録済みレシピのテスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 1. 既存レシピ登録
    existing_recipe_data = {
        "recipe_name": "クックパッドの唐揚げ",
        "recipe_type": "existing",
        "recipe_url": "https://cookpad.com/recipe/123456"
    }
    
    response = requests.post(f"{BASE_URL}/api/web/registered-recipes/", json=existing_recipe_data, headers=headers)
    print(f"既存レシピ登録: {response.status_code}")
    if response.status_code == 201:
        print("✅ 既存レシピ登録成功")
    else:
        print(f"❌ 既存レシピ登録失敗: {response.text}")
    
    # 2. 新規レシピ登録
    new_recipe_data = {
        "recipe_name": "親子丼（改良版）",
        "recipe_type": "new",
        "recipe": recipe_id
    }
    
    response = requests.post(f"{BASE_URL}/api/web/registered-recipes/", json=new_recipe_data, headers=headers)
    print(f"新規レシピ登録: {response.status_code}")
    if response.status_code == 201:
        registered_recipe = response.json()
        registered_recipe_id = registered_recipe["id"]
        print(f"✅ 新規レシピ登録成功: ID={registered_recipe_id}")
        return registered_recipe_id
    else:
        print(f"❌ 新規レシピ登録失敗: {response.text}")
        return None

def test_cooked_dish(access_token, registered_recipe_id):
    """料理履歴のテスト"""
    print("\n=== 料理履歴のテスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 料理履歴作成
    cooked_data = {
        "registered_recipe": registered_recipe_id
    }
    
    response = requests.post(f"{BASE_URL}/api/web/cooked-dishes/", json=cooked_data, headers=headers)
    print(f"料理履歴作成: {response.status_code}")
    if response.status_code == 201:
        cooked = response.json()
        print(f"✅ 料理履歴作成成功: {cooked['registered_recipe_detail']['recipe_name']}")
    else:
        print(f"❌ 料理履歴作成失敗: {response.text}")

def test_dashboard(access_token):
    """ダッシュボードのテスト"""
    print("\n=== ダッシュボードのテスト ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/api/web/dashboard/", headers=headers)
    print(f"ダッシュボード取得: {response.status_code}")
    if response.status_code == 200:
        dashboard = response.json()
        print("✅ ダッシュボード取得成功")
        print(f"   レシピ数: {dashboard['stats']['total_recipes']}")
        print(f"   登録済みレシピ数: {dashboard['stats']['total_registered_recipes']}")
        print(f"   料理履歴数: {dashboard['stats']['total_cooked_dishes']}")
    else:
        print(f"❌ ダッシュボード取得失敗: {response.text}")

def setup_api_key():
    """API Keyを設定（Django管理画面または直接DB操作で事前に作成が必要）"""
    print("\n=== API Key設定の説明 ===")
    print("外部APIテストには事前にAPI Keyの作成が必要です：")
    print("1. python manage.py shell")
    print("2. from daily_dish.models import ApiKey")
    print("3. ApiKey.objects.create(key_name='テスト用', api_key='test-key-12345')")
    return "test-key-12345"

def test_external_api():
    """外部APIのテスト"""
    print("\n=== 外部APIのテスト ===")
    
    api_key = "test-key-12345"
    headers = {"X-API-KEY": api_key}
    
    # 統計情報取得
    response = requests.get(f"{BASE_URL}/api/external/stats/", headers=headers)
    print(f"外部API 統計情報: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print("✅ 外部API統計情報取得成功")
        print(f"   総レシピ数: {stats['total_recipes']}")
        print(f"   総ユーザー数: {stats['total_users']}")
    else:
        print(f"❌ 外部API統計情報取得失敗: {response.text}")
        print("注意: API Keyが事前に作成されている必要があります")

def main():
    """メインテスト実行"""
    print("Daily Dish API テスト開始")
    print("=" * 50)
    
    # Web API テスト
    access_token, refresh_token = test_user_registration_and_login()
    if access_token:
        recipe_id = test_recipe_crud(access_token)
        if recipe_id:
            registered_recipe_id = test_registered_recipe(access_token, recipe_id)
            if registered_recipe_id:
                test_cooked_dish(access_token, registered_recipe_id)
        test_dashboard(access_token)
    
    # 外部API テスト
    setup_api_key()
    test_external_api()
    
    print("\n" + "=" * 50)
    print("テスト完了")

if __name__ == "__main__":
    main()