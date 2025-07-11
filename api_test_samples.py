#!/usr/bin/env python3
"""
Daily Dish API テストサンプル
Railway デプロイ後のAPI動作確認用
"""
import requests
import json

# Railway URL
BASE_URL = "https://web-production-889e.up.railway.app"
API_BASE = f"{BASE_URL}/api"

class DailyDishAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.api_key = None
    
    def test_1_user_registration(self):
        """テスト1: ユーザー登録"""
        print("=== テスト1: ユーザー登録 ===")
        
        url = f"{self.base_url}/web/auth/register/"
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123"
        }
        
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ ユーザー登録成功")
            return True
        else:
            print("❌ ユーザー登録失敗")
            return False
    
    def test_2_user_login(self):
        """テスト2: ログイン（JWT取得）"""
        print("\n=== テスト2: ユーザーログイン ===")
        
        url = f"{self.base_url}/web/auth/login/"
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            self.access_token = response.json().get("access")
            print(f"✅ ログイン成功")
            print(f"Access Token: {self.access_token[:50]}...")
            
            # 以降のリクエスト用にヘッダー設定
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            })
            return True
        else:
            print("❌ ログイン失敗")
            return False
    
    def test_3_create_new_recipe(self):
        """テスト3: 新規レシピ作成"""
        print("\n=== テスト3: 新規レシピ作成 ===")
        
        url = f"{self.base_url}/web/recipes/"
        data = {
            "recipe_name": "手作りハンバーグ",
            "ingredient_1": "牛ひき肉",
            "amount_1": 400.0,
            "unit_1": "g",
            "ingredient_2": "玉ねぎ",
            "amount_2": 1.0,
            "unit_2": "個",
            "ingredient_3": "パン粉",
            "amount_3": 50.0,
            "unit_3": "g",
            "ingredient_4": "卵",
            "amount_4": 1.0,
            "unit_4": "個"
        }
        
        response = self.session.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            recipe_id = response.json().get("id")
            print(f"✅ 新規レシピ作成成功 (ID: {recipe_id})")
            return recipe_id
        else:
            print("❌ 新規レシピ作成失敗")
            return None
    
    def test_4_create_existing_recipe(self):
        """テスト4: 既存レシピ作成（URL付き）"""
        print("\n=== テスト4: 既存レシピ作成 ===")
        
        url = f"{self.base_url}/web/recipes/"
        data = {
            "recipe_name": "クックパッドのチキンカレー",
            "recipe_url": "https://cookpad.com/recipe/123456",
            "ingredient_1": "鶏肉",
            "amount_1": 300.0,
            "unit_1": "g",
            "ingredient_2": "じゃがいも",
            "amount_2": 2.0,
            "unit_2": "個",
            "ingredient_3": "人参",
            "amount_3": 1.0,
            "unit_3": "本",
            "ingredient_4": "カレールー",
            "amount_4": 4.0,
            "unit_4": "かけ"
        }
        
        response = self.session.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            recipe_id = response.json().get("id")
            print(f"✅ 既存レシピ作成成功 (ID: {recipe_id})")
            return recipe_id
        else:
            print("❌ 既存レシピ作成失敗")
            return None
    
    def test_5_get_recipes(self):
        """テスト5: レシピ一覧取得"""
        print("\n=== テスト5: レシピ一覧取得 ===")
        
        url = f"{self.base_url}/web/recipes/"
        response = self.session.get(url)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            recipes = response.json().get("results", [])
            print(f"✅ レシピ一覧取得成功 ({len(recipes)}件)")
            return recipes
        else:
            print("❌ レシピ一覧取得失敗")
            return None
    
    def test_6_create_cooked_dish(self, recipe_id):
        """テスト6: 料理履歴作成"""
        print(f"\n=== テスト6: 料理履歴作成 (Recipe ID: {recipe_id}) ===")
        
        url = f"{self.base_url}/web/cooked-dishes/"
        data = {
            "recipe": recipe_id
        }
        
        response = self.session.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            print("✅ 料理履歴作成成功")
            return True
        else:
            print("❌ 料理履歴作成失敗")
            return False
    
    def test_7_user_stats(self):
        """テスト7: ユーザー統計情報取得"""
        print("\n=== テスト7: ユーザー統計情報取得 ===")
        
        url = f"{self.base_url}/web/stats/"
        response = self.session.get(url)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ ユーザー統計取得成功")
            return True
        else:
            print("❌ ユーザー統計取得失敗")
            return False

def run_all_tests():
    """全テストを実行"""
    print("Daily Dish API テスト開始")
    print("=" * 50)
    
    # URLを実際のRailway URLに変更してください
    api_url = f"{API_BASE}"
    tester = DailyDishAPITester(api_url)
    
    # テスト実行
    tests_results = []
    
    # 1. ユーザー登録
    tests_results.append(tester.test_1_user_registration())
    
    # 2. ログイン
    login_success = tester.test_2_user_login()
    tests_results.append(login_success)
    
    if login_success:
        # 3. 新規レシピ作成
        recipe_id_1 = tester.test_3_create_new_recipe()
        tests_results.append(recipe_id_1 is not None)
        
        # 4. 既存レシピ作成
        recipe_id_2 = tester.test_4_create_existing_recipe()
        tests_results.append(recipe_id_2 is not None)
        
        # 5. レシピ一覧取得
        tests_results.append(tester.test_5_get_recipes() is not None)
        
        # 6. 料理履歴作成
        if recipe_id_1:
            tests_results.append(tester.test_6_create_cooked_dish(recipe_id_1))
        
        # 7. ユーザー統計
        tests_results.append(tester.test_7_user_stats())
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("テスト結果サマリー")
    print("=" * 50)
    success_count = sum(tests_results)
    total_count = len(tests_results)
    print(f"成功: {success_count}/{total_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 全テスト成功！Daily Dish APIは正常に動作しています！")
    else:
        print("⚠️  一部のテストが失敗しました。詳細を確認してください。")

if __name__ == "__main__":
    print("Daily Dish API テストツール")
    print("使用前に BASE_URL を実際のRailway URLに変更してください")
    print()
    
    # URLの確認
    print(f"現在の設定URL: {BASE_URL}")
    answer = input("このURLで実行しますか？ (URLを変更する場合は'n')  [y/n]: ")
    
    if answer.lower() == 'n':
        new_url = input("新しいURLを入力してください: ")
        BASE_URL = new_url
        API_BASE = f"{BASE_URL}/api"
    
    run_all_tests()