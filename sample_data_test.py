#!/usr/bin/env python3
"""
サンプルデータテスト実行スクリプト

Daily Dishの主要機能をサンプルデータでテストし、
DB状態を確認して想定結果と実行結果を比較します。
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

class TestExecutor:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        self.recipe_id = None
        self.registered_recipe_ids = []
        
    def log_test_case(self, test_case, description):
        """テストケースのログ出力"""
        print(f"\n{'='*60}")
        print(f"テストケース: {test_case}")
        print(f"内容: {description}")
        print(f"{'='*60}")
    
    def log_request(self, method, url, data=None):
        """リクエストのログ出力"""
        print(f"\n📤 REQUEST:")
        print(f"   Method: {method}")
        print(f"   URL: {url}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    def log_response(self, response):
        """レスポンスのログ出力"""
        print(f"\n📥 RESPONSE:")
        print(f"   Status: {response.status_code}")
        try:
            response_data = response.json()
            print(f"   Data: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            return response_data
        except:
            print(f"   Data: {response.text}")
            return None
    
    def tc001_user_registration(self):
        """TC001: ユーザー登録テスト"""
        self.log_test_case("TC001", "ユーザー登録テスト")
        
        print("\n🔍 想定結果（DB）:")
        print("   - usersテーブルに新規レコード追加")
        print("   - username: 'yamada_taro'")
        print("   - email: 'yamada@example.com'")
        print("   - is_active: true")
        print("   - created_at: 実行時刻")
        print("   - updated_at: 実行時刻")
        
        user_data = {
            "username": "yamada_taro",
            "email": "yamada@example.com",
            "password": "securepassword123",
            "password_confirm": "securepassword123"
        }
        
        url = f"{BASE_URL}/api/web/auth/register/"
        self.log_request("POST", url, user_data)
        
        response = requests.post(url, json=user_data)
        response_data = self.log_response(response)
        
        if response.status_code == 201:
            print("✅ ユーザー登録成功")
            
            # ログインしてトークン取得
            login_data = {
                "username": "yamada_taro",
                "password": "securepassword123"
            }
            login_response = requests.post(f"{BASE_URL}/api/web/auth/login/", json=login_data)
            if login_response.status_code == 200:
                tokens = login_response.json()
                self.access_token = tokens["access"]
                
                # プロフィール取得でuser_id確認
                headers = {"Authorization": f"Bearer {self.access_token}"}
                profile_response = requests.get(f"{BASE_URL}/api/web/auth/profile/", headers=headers)
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    self.user_id = profile["id"]
                    print(f"   取得したユーザーID: {self.user_id}")
                
        else:
            print(f"❌ ユーザー登録失敗: {response.text}")
        
        return response.status_code == 201
    
    def tc002_new_recipe_registration(self):
        """TC002: 新規レシピ登録テスト"""
        self.log_test_case("TC002", "新規レシピ登録テスト")
        
        print("\n🔍 想定結果（DB）:")
        print("   - recipesテーブルに新規レコード追加")
        print(f"   - user_id: {self.user_id}")
        print("   - recipe_name: '山田家の肉じゃが'")
        print("   - ingredient_1: 'じゃがいも', amount_1: 4.0, unit_1: '個'")
        print("   - ingredient_2: 'にんじん', amount_2: 1.0, unit_2: '本'")
        print("   - ingredient_3: '玉ねぎ', amount_3: 1.0, unit_3: '個'")
        print("   - ingredient_4: '牛肉', amount_4: 300.0, unit_4: 'g'")
        print("   - ingredient_5: 'しらたき', amount_5: 1.0, unit_5: '袋'")
        print("   - ingredient_6〜20: NULL")
        
        recipe_data = {
            "recipe_name": "山田家の肉じゃが",
            "ingredient_1": "じゃがいも",
            "amount_1": "4.0",
            "unit_1": "個",
            "ingredient_2": "にんじん",
            "amount_2": "1.0",
            "unit_2": "本",
            "ingredient_3": "玉ねぎ",
            "amount_3": "1.0",
            "unit_3": "個",
            "ingredient_4": "牛肉",
            "amount_4": "300.0",
            "unit_4": "g",
            "ingredient_5": "しらたき",
            "amount_5": "1.0",
            "unit_5": "袋"
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{BASE_URL}/api/web/recipes/"
        self.log_request("POST", url, recipe_data)
        
        response = requests.post(url, json=recipe_data, headers=headers)
        response_data = self.log_response(response)
        
        if response.status_code == 201:
            print("✅ レシピ作成成功")
            self.recipe_id = response_data["id"]
            print(f"   作成されたレシピID: {self.recipe_id}")
            
            # 材料確認
            ingredients = response_data.get("ingredients", [])
            print(f"   登録された材料数: {len(ingredients)}")
            for i, ingredient in enumerate(ingredients, 1):
                print(f"   材料{i}: {ingredient['name']} {ingredient['amount']}{ingredient['unit']}")
        else:
            print(f"❌ レシピ作成失敗: {response.text}")
        
        return response.status_code == 201
    
    def tc003_existing_recipe_registration(self):
        """TC003: 既存レシピ登録テスト"""
        self.log_test_case("TC003", "既存レシピ登録テスト")
        
        print("\n🔍 想定結果（DB）:")
        print("   - registered_recipesテーブルに新規レコード追加")
        print(f"   - user_id: {self.user_id}")
        print("   - recipe_name: 'クックパッドの鶏の唐揚げ'")
        print("   - recipe_type: 'existing'")
        print("   - recipe_url: 'https://cookpad.com/recipe/2858078'")
        print("   - recipe_id: NULL")
        
        registered_recipe_data = {
            "recipe_name": "クックパッドの鶏の唐揚げ",
            "recipe_type": "existing",
            "recipe_url": "https://cookpad.com/recipe/2858078"
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{BASE_URL}/api/web/registered-recipes/"
        self.log_request("POST", url, registered_recipe_data)
        
        response = requests.post(url, json=registered_recipe_data, headers=headers)
        response_data = self.log_response(response)
        
        if response.status_code == 201:
            print("✅ 既存レシピ登録成功")
            registered_id = response_data["id"]
            self.registered_recipe_ids.append(registered_id)
            print(f"   登録済みレシピID: {registered_id}")
        else:
            print(f"❌ 既存レシピ登録失敗: {response.text}")
        
        return response.status_code == 201
    
    def tc004_new_recipe_to_registered(self):
        """TC004: 新規レシピの登録済みレシピ化テスト"""
        self.log_test_case("TC004", "新規レシピの登録済みレシピ化テスト")
        
        print("\n🔍 想定結果（DB）:")
        print("   - registered_recipesテーブルに新規レコード追加")
        print(f"   - user_id: {self.user_id}")
        print("   - recipe_name: '山田家の肉じゃが'")
        print("   - recipe_type: 'new'")
        print("   - recipe_url: NULL")
        print(f"   - recipe_id: {self.recipe_id}")
        
        registered_recipe_data = {
            "recipe_name": "山田家の肉じゃが",
            "recipe_type": "new",
            "recipe": self.recipe_id
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{BASE_URL}/api/web/registered-recipes/"
        self.log_request("POST", url, registered_recipe_data)
        
        response = requests.post(url, json=registered_recipe_data, headers=headers)
        response_data = self.log_response(response)
        
        if response.status_code == 201:
            print("✅ 新規レシピの登録済みレシピ化成功")
            registered_id = response_data["id"]
            self.registered_recipe_ids.append(registered_id)
            print(f"   登録済みレシピID: {registered_id}")
            
            # レシピ詳細確認
            recipe_detail = response_data.get("recipe_detail")
            if recipe_detail:
                print(f"   関連レシピ名: {recipe_detail['recipe_name']}")
                print(f"   材料数: {len(recipe_detail.get('ingredients', []))}")
        else:
            print(f"❌ 新規レシピの登録済みレシピ化失敗: {response.text}")
        
        return response.status_code == 201
    
    def tc005_ingredient_cache_registration(self):
        """TC005: 食材キャッシュ登録テスト"""
        self.log_test_case("TC005", "食材キャッシュ登録テスト")
        
        print("\n🔍 想定結果（DB）:")
        print("   - ingredient_cacheテーブルに5件のレコード追加")
        print(f"   - user_id: {self.user_id} (全レコード)")
        print("   - じゃがいも 4.0個")
        print("   - にんじん 1.0本") 
        print("   - 玉ねぎ 1.0個")
        print("   - 牛肉 300.0g")
        print("   - しらたき 1.0袋")
        
        ingredients = [
            {"ingredient_name": "じゃがいも", "amount": "4.0", "unit": "個"},
            {"ingredient_name": "にんじん", "amount": "1.0", "unit": "本"},
            {"ingredient_name": "玉ねぎ", "amount": "1.0", "unit": "個"},
            {"ingredient_name": "牛肉", "amount": "300.0", "unit": "g"},
            {"ingredient_name": "しらたき", "amount": "1.0", "unit": "袋"}
        ]
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{BASE_URL}/api/web/ingredient-cache/"
        
        success_count = 0
        for ingredient in ingredients:
            self.log_request("POST", url, ingredient)
            response = requests.post(url, json=ingredient, headers=headers)
            response_data = self.log_response(response)
            
            if response.status_code == 201:
                success_count += 1
                print(f"✅ 食材キャッシュ登録成功: {ingredient['ingredient_name']}")
            else:
                print(f"❌ 食材キャッシュ登録失敗: {ingredient['ingredient_name']} - {response.text}")
        
        print(f"\n登録成功件数: {success_count}/5")
        return success_count == 5
    
    def verify_final_state(self):
        """最終状態確認"""
        self.log_test_case("VERIFY", "最終データ状態確認")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # ダッシュボード確認
        dashboard_response = requests.get(f"{BASE_URL}/api/web/dashboard/", headers=headers)
        if dashboard_response.status_code == 200:
            dashboard = dashboard_response.json()
            stats = dashboard["stats"]
            
            print("\n📊 最終統計:")
            print(f"   レシピ数: {stats['total_recipes']}")
            print(f"   登録済みレシピ数: {stats['total_registered_recipes']}")
            print(f"   料理履歴数: {stats['total_cooked_dishes']}")
            print(f"   食材キャッシュ数: {stats['total_ingredient_cache']}")
        
        # レシピ一覧確認
        recipes_response = requests.get(f"{BASE_URL}/api/web/recipes/", headers=headers)
        if recipes_response.status_code == 200:
            recipes = recipes_response.json()
            print(f"\n📝 レシピ一覧（{recipes['count']}件）:")
            for recipe in recipes['results']:
                print(f"   ID{recipe['id']}: {recipe['recipe_name']}")
        
        # 登録済みレシピ一覧確認
        registered_response = requests.get(f"{BASE_URL}/api/web/registered-recipes/", headers=headers)
        if registered_response.status_code == 200:
            registered = registered_response.json()
            print(f"\n📋 登録済みレシピ一覧（{registered['count']}件）:")
            for reg in registered['results']:
                print(f"   ID{reg['id']}: {reg['recipe_name']} ({reg['recipe_type']})")
        
        # 食材キャッシュ一覧確認
        cache_response = requests.get(f"{BASE_URL}/api/web/ingredient-cache/", headers=headers)
        if cache_response.status_code == 200:
            cache = cache_response.json()
            print(f"\n🛒 食材キャッシュ一覧（{cache['count']}件）:")
            for item in cache['results']:
                print(f"   {item['ingredient_name']}: {item['amount']}{item['unit']}")

def main():
    """メインテスト実行"""
    print("Daily Dish サンプルデータテスト開始")
    print(f"開始時刻: {datetime.now()}")
    
    executor = TestExecutor()
    
    # テスト実行
    test_results = []
    
    test_results.append(("TC001", "ユーザー登録", executor.tc001_user_registration()))
    if test_results[-1][2]:  # 前のテストが成功した場合のみ次へ
        test_results.append(("TC002", "新規レシピ登録", executor.tc002_new_recipe_registration()))
    
    if test_results[-1][2]:
        test_results.append(("TC003", "既存レシピ登録", executor.tc003_existing_recipe_registration()))
    
    if test_results[-1][2]:
        test_results.append(("TC004", "新規レシピの登録済み化", executor.tc004_new_recipe_to_registered()))
    
    if test_results[-1][2]:
        test_results.append(("TC005", "食材キャッシュ登録", executor.tc005_ingredient_cache_registration()))
    
    # 最終確認
    if all(result[2] for result in test_results):
        executor.verify_final_state()
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print("テスト結果サマリー")
    print(f"{'='*60}")
    
    for test_id, description, result in test_results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_id}: {description} - {status}")
    
    success_count = sum(1 for _, _, result in test_results if result)
    print(f"\n成功: {success_count}/{len(test_results)}")
    print(f"終了時刻: {datetime.now()}")

if __name__ == "__main__":
    main()