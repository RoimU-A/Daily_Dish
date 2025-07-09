#!/usr/bin/env python3
"""
Daily Dish API 実行例集
各APIの実際の使用例をまとめたサンプルコード
"""

import requests
import json
import subprocess

# 設定
def get_ngrok_url():
    """ngrok URLを自動取得"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:4040/api/tunnels'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data['tunnels']:
                return data['tunnels'][0]['public_url']
    except:
        pass
    return None

BASE_URL = get_ngrok_url()
if not BASE_URL:
    print("❌ ngrok URLを取得できませんでした")
    exit(1)

print(f"🌐 Base URL: {BASE_URL}")

# テストデータ
TEST_USER = {
    "username": "testuser_v2",
    "password": "testpassword123"
}
API_KEY = "test-api-key-v2-12345"

class DailyDishAPI:
    """Daily Dish API クライアント"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.api_key = API_KEY
    
    def login(self, username, password):
        """ログイン"""
        url = f"{self.base_url}/api/web/auth/login/"
        data = {"username": username, "password": password}
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.access_token = response.json()['access']
            print(f"✅ ログイン成功: {username}")
            return True
        else:
            print(f"❌ ログイン失敗: {response.status_code}")
            return False
    
    def get_headers(self, auth_type='jwt'):
        """認証ヘッダーを取得"""
        if auth_type == 'jwt':
            return {"Authorization": f"Bearer {self.access_token}"}
        elif auth_type == 'api_key':
            return {"X-API-KEY": self.api_key}
        return {}
    
    # === レシピ管理 ===
    def create_existing_recipe(self, recipe_name, recipe_url, ingredients):
        """既存レシピ作成"""
        url = f"{self.base_url}/api/web/recipes/"
        data = {
            "recipe_name": recipe_name,
            "recipe_url": recipe_url
        }
        
        # 材料を追加
        for i, ingredient in enumerate(ingredients, 1):
            data[f"ingredient_{i}"] = ingredient['name']
            data[f"amount_{i}"] = ingredient['amount']
            data[f"unit_{i}"] = ingredient['unit']
        
        response = requests.post(url, json=data, headers=self.get_headers())
        return response
    
    def create_new_recipe(self, recipe_name, ingredients):
        """新規レシピ作成"""
        url = f"{self.base_url}/api/web/recipes/"
        data = {"recipe_name": recipe_name}
        
        # 材料を追加
        for i, ingredient in enumerate(ingredients, 1):
            data[f"ingredient_{i}"] = ingredient['name']
            data[f"amount_{i}"] = ingredient['amount']
            data[f"unit_{i}"] = ingredient['unit']
        
        response = requests.post(url, json=data, headers=self.get_headers())
        return response
    
    def get_recipes(self):
        """レシピ一覧取得"""
        url = f"{self.base_url}/api/web/recipes/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    def get_recipe(self, recipe_id):
        """レシピ詳細取得"""
        url = f"{self.base_url}/api/web/recipes/{recipe_id}/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    def update_recipe(self, recipe_id, recipe_data):
        """レシピ更新"""
        url = f"{self.base_url}/api/web/recipes/{recipe_id}/"
        response = requests.put(url, json=recipe_data, headers=self.get_headers())
        return response
    
    def delete_recipe(self, recipe_id):
        """レシピ削除"""
        url = f"{self.base_url}/api/web/recipes/{recipe_id}/"
        response = requests.delete(url, headers=self.get_headers())
        return response
    
    # === 料理履歴管理 ===
    def cook_recipe(self, recipe_id):
        """料理履歴登録"""
        url = f"{self.base_url}/api/web/cooked-dishes/"
        data = {"recipe": recipe_id}
        response = requests.post(url, json=data, headers=self.get_headers())
        return response
    
    def get_cooked_dishes(self):
        """料理履歴一覧取得"""
        url = f"{self.base_url}/api/web/cooked-dishes/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    def delete_cooked_dish(self, dish_id):
        """料理履歴削除"""
        url = f"{self.base_url}/api/web/cooked-dishes/{dish_id}/"
        response = requests.delete(url, headers=self.get_headers())
        return response
    
    # === 食材キャッシュ管理 ===
    def add_ingredient_cache(self, ingredient_name, amount, unit):
        """食材キャッシュ追加"""
        url = f"{self.base_url}/api/web/ingredient-cache/"
        data = {
            "ingredient_name": ingredient_name,
            "amount": amount,
            "unit": unit
        }
        response = requests.post(url, json=data, headers=self.get_headers())
        return response
    
    def get_ingredient_cache(self):
        """食材キャッシュ一覧取得"""
        url = f"{self.base_url}/api/web/ingredient-cache/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    # === 統計情報 ===
    def get_user_stats(self):
        """ユーザー統計取得"""
        url = f"{self.base_url}/api/web/stats/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    def get_dashboard(self):
        """ダッシュボード取得"""
        url = f"{self.base_url}/api/web/dashboard/"
        response = requests.get(url, headers=self.get_headers())
        return response
    
    # === 外部API ===
    def get_external_stats(self):
        """外部API統計取得"""
        url = f"{self.base_url}/api/external/stats/"
        response = requests.get(url, headers=self.get_headers('api_key'))
        return response
    
    def get_external_recipes(self):
        """外部API レシピ一覧取得"""
        url = f"{self.base_url}/api/external/recipes/"
        response = requests.get(url, headers=self.get_headers('api_key'))
        return response

def example_basic_usage():
    """基本的な使用例"""
    print("\n=== 基本的な使用例 ===")
    
    # APIクライアント初期化
    api = DailyDishAPI(BASE_URL)
    
    # ログイン
    if not api.login(TEST_USER['username'], TEST_USER['password']):
        return
    
    # 既存レシピ作成
    print("\n1. 既存レシピ作成")
    ingredients = [
        {"name": "鶏胸肉", "amount": 300.0, "unit": "g"},
        {"name": "ブロッコリー", "amount": 1.0, "unit": "房"},
        {"name": "オリーブオイル", "amount": 15.0, "unit": "ml"}
    ]
    
    response = api.create_existing_recipe(
        "ヘルシーチキンソテー",
        "https://example.com/recipe/healthy-chicken",
        ingredients
    )
    
    if response.status_code == 201:
        recipe_data = response.json()
        print(f"✅ 既存レシピ作成成功: {recipe_data['recipe_name']}")
        recipe_id = recipe_data['id']
        
        # 料理履歴登録
        print("\n2. 料理履歴登録")
        cook_response = api.cook_recipe(recipe_id)
        if cook_response.status_code == 201:
            print(f"✅ 料理履歴登録成功")
        
        # レシピ一覧取得
        print("\n3. レシピ一覧取得")
        recipes_response = api.get_recipes()
        if recipes_response.status_code == 200:
            recipes = recipes_response.json()
            print(f"✅ レシピ一覧取得成功: {recipes['count']}件")
    
    # 統計情報取得
    print("\n4. 統計情報取得")
    stats_response = api.get_user_stats()
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"✅ 統計情報: レシピ{stats['total_recipes']}件, 料理履歴{stats['total_cooked_dishes']}件")

def example_advanced_usage():
    """高度な使用例"""
    print("\n=== 高度な使用例 ===")
    
    api = DailyDishAPI(BASE_URL)
    
    if not api.login(TEST_USER['username'], TEST_USER['password']):
        return
    
    # 新規レシピ作成
    print("\n1. 新規レシピ作成")
    ingredients = [
        {"name": "豚バラ肉", "amount": 400.0, "unit": "g"},
        {"name": "キャベツ", "amount": 0.5, "unit": "個"},
        {"name": "もやし", "amount": 1.0, "unit": "袋"}
    ]
    
    response = api.create_new_recipe("手作り野菜炒め", ingredients)
    if response.status_code == 201:
        recipe_data = response.json()
        print(f"✅ 新規レシピ作成成功: {recipe_data['recipe_name']}")
        
        # レシピ更新
        print("\n2. レシピ更新")
        updated_data = {
            "recipe_name": "手作り野菜炒め（改良版）",
            "ingredient_1": "豚バラ肉", "amount_1": 350.0, "unit_1": "g",
            "ingredient_2": "キャベツ", "amount_2": 0.5, "unit_2": "個",
            "ingredient_3": "もやし", "amount_3": 1.0, "unit_3": "袋",
            "ingredient_4": "ニンジン", "amount_4": 0.5, "unit_4": "本"
        }
        
        update_response = api.update_recipe(recipe_data['id'], updated_data)
        if update_response.status_code == 200:
            print(f"✅ レシピ更新成功")
    
    # 食材キャッシュ管理
    print("\n3. 食材キャッシュ管理")
    cache_response = api.add_ingredient_cache("豚バラ肉", 500.0, "g")
    if cache_response.status_code == 201:
        print(f"✅ 食材キャッシュ追加成功")
    
    # 外部API使用
    print("\n4. 外部API使用")
    external_stats = api.get_external_stats()
    if external_stats.status_code == 200:
        stats = external_stats.json()
        print(f"✅ 外部API統計: 全レシピ{stats['total_recipes']}件, 全ユーザー{stats['total_users']}人")

def example_error_handling():
    """エラーハンドリング例"""
    print("\n=== エラーハンドリング例 ===")
    
    api = DailyDishAPI(BASE_URL)
    
    # 認証エラー
    print("\n1. 認証エラーテスト")
    response = api.get_recipes()  # ログイン前にアクセス
    if response.status_code == 401:
        print(f"✅ 認証エラー正常検出: {response.status_code}")
    
    # ログイン
    api.login(TEST_USER['username'], TEST_USER['password'])
    
    # 存在しないリソース
    print("\n2. 存在しないリソースアクセス")
    response = api.get_recipe(99999)  # 存在しないID
    if response.status_code == 404:
        print(f"✅ 404エラー正常検出: {response.status_code}")
    
    # バリデーションエラー
    print("\n3. バリデーションエラー")
    invalid_ingredients = []  # 材料なし
    response = api.create_new_recipe("無効レシピ", invalid_ingredients)
    if response.status_code == 400:
        print(f"✅ バリデーションエラー正常検出: {response.status_code}")
        print(f"   エラー内容: {response.json()}")

def main():
    """メイン実行"""
    print("Daily Dish API 実行例集")
    print("=" * 40)
    
    # 基本的な使用例
    example_basic_usage()
    
    # 高度な使用例
    example_advanced_usage()
    
    # エラーハンドリング例
    example_error_handling()
    
    print("\n" + "=" * 40)
    print("全ての例の実行完了！")
    print("詳細なログは http://localhost:4040 で確認できます")

if __name__ == "__main__":
    main()