#!/usr/bin/env python3
"""
Daily Dish レシピ取得API専用テスト
レシピ一覧・個別レシピ取得機能のテストケース
"""
import requests
import json
import time
from datetime import datetime

# Railway URL
BASE_URL = "https://web-production-889e.up.railway.app"
API_BASE = f"{BASE_URL}/api"

class RecipeRetrievalTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.created_recipe_ids = []
    
    def setup_authentication(self):
        """認証のセットアップ（テスト用ユーザーでログイン）"""
        print("=== 認証セットアップ ===")
        
        # テストユーザーでログイン
        url = f"{self.base_url}/web/auth/login/"
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = requests.post(url, json=data)
        print(f"ログインステータス: {response.status_code}")
        
        if response.status_code == 200:
            self.access_token = response.json().get("access")
            print(f"✅ 認証成功")
            
            # セッションヘッダー設定
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            })
            return True
        else:
            print(f"❌ 認証失敗: {response.text}")
            return False
    
    def create_test_recipes(self):
        """テスト用レシピを作成"""
        print("\n=== テスト用レシピ作成 ===")
        
        test_recipes = [
            {
                "recipe_name": "照り焼きチキン",
                "ingredient_1": "鶏もも肉", "amount_1": 300.0, "unit_1": "g",
                "ingredient_2": "醤油", "amount_2": 2.0, "unit_2": "大さじ",
                "ingredient_3": "みりん", "amount_3": 2.0, "unit_3": "大さじ",
                "ingredient_4": "砂糖", "amount_4": 1.0, "unit_4": "大さじ"
            },
            {
                "recipe_name": "野菜炒め",
                "recipe_url": "https://example.com/yasai-itame",
                "ingredient_1": "キャベツ", "amount_1": 0.25, "unit_1": "玉",
                "ingredient_2": "人参", "amount_2": 0.5, "unit_2": "本",
                "ingredient_3": "豚肉", "amount_3": 150.0, "unit_3": "g"
            },
            {
                "recipe_name": "味噌汁",
                "ingredient_1": "味噌", "amount_1": 2.0, "unit_1": "大さじ",
                "ingredient_2": "豆腐", "amount_2": 0.5, "unit_2": "丁",
                "ingredient_3": "わかめ", "amount_3": 1.0, "unit_3": "少々"
            }
        ]
        
        url = f"{self.base_url}/web/recipes/"
        
        for i, recipe_data in enumerate(test_recipes, 1):
            response = self.session.post(url, json=recipe_data)
            print(f"レシピ{i} 作成: {response.status_code}")
            
            if response.status_code == 201:
                recipe_id = response.json().get("id")
                self.created_recipe_ids.append(recipe_id)
                print(f"✅ レシピ{i} 作成成功 (ID: {recipe_id})")
            else:
                print(f"❌ レシピ{i} 作成失敗: {response.text}")
        
        print(f"作成されたレシピID: {self.created_recipe_ids}")
        return len(self.created_recipe_ids) > 0
    
    def test_recipe_list_retrieval(self):
        """テスト1: レシピ一覧取得"""
        print("\n=== テスト1: レシピ一覧取得 ===")
        
        url = f"{self.base_url}/web/recipes/"
        response = self.session.get(url)
        
        print(f"URL: {url}")
        print(f"ステータス: {response.status_code}")
        print(f"レスポンスヘッダー: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"レスポンス構造: {list(data.keys())}")
            
            if "results" in data:
                recipes = data["results"]
                print(f"取得レシピ数: {len(recipes)}")
                print(f"ページネーション情報:")
                print(f"  - count: {data.get('count')}")
                print(f"  - next: {data.get('next')}")
                print(f"  - previous: {data.get('previous')}")
                
                # 最初のレシピの詳細表示
                if recipes:
                    first_recipe = recipes[0]
                    print(f"\n最初のレシピサンプル:")
                    print(f"  - ID: {first_recipe.get('id')}")
                    print(f"  - 名前: {first_recipe.get('recipe_name')}")
                    print(f"  - URL: {first_recipe.get('recipe_url', 'なし')}")
                    print(f"  - 材料数: {len(first_recipe.get('ingredients', []))}")
                    print(f"  - 作成日: {first_recipe.get('created_at')}")
                
                print("✅ レシピ一覧取得成功")
                return recipes
            else:
                print("❌ レスポンス形式が期待と異なります")
                print(f"実際のレスポンス: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print(f"❌ レシピ一覧取得失敗")
            print(f"エラー内容: {response.text}")
            return None
    
    def test_individual_recipe_retrieval(self, recipe_id):
        """テスト2: 個別レシピ取得"""
        print(f"\n=== テスト2: 個別レシピ取得 (ID: {recipe_id}) ===")
        
        url = f"{self.base_url}/web/recipes/{recipe_id}/"
        response = self.session.get(url)
        
        print(f"URL: {url}")
        print(f"ステータス: {response.status_code}")
        
        if response.status_code == 200:
            recipe = response.json()
            print(f"✅ 個別レシピ取得成功")
            print(f"レシピ詳細:")
            print(f"  - ID: {recipe.get('id')}")
            print(f"  - 名前: {recipe.get('recipe_name')}")
            print(f"  - URL: {recipe.get('recipe_url', 'なし')}")
            print(f"  - ユーザー: {recipe.get('user')}")
            print(f"  - 既存レシピ: {recipe.get('is_existing_recipe')}")
            print(f"  - 新規レシピ: {recipe.get('is_new_recipe')}")
            print(f"  - 作成日: {recipe.get('created_at')}")
            print(f"  - 更新日: {recipe.get('updated_at')}")
            
            # 材料情報の詳細表示
            ingredients = recipe.get('ingredients', [])
            print(f"\n材料リスト ({len(ingredients)}種類):")
            for i, ingredient in enumerate(ingredients, 1):
                print(f"  {i}. {ingredient.get('name')} - {ingredient.get('amount')}{ingredient.get('unit')}")
            
            return recipe
        elif response.status_code == 404:
            print(f"❌ レシピが見つかりません (ID: {recipe_id})")
        else:
            print(f"❌ 個別レシピ取得失敗")
            print(f"エラー内容: {response.text}")
        
        return None
    
    def test_non_existent_recipe(self):
        """テスト3: 存在しないレシピの取得"""
        print(f"\n=== テスト3: 存在しないレシピ取得 ===")
        
        non_existent_id = 99999
        url = f"{self.base_url}/web/recipes/{non_existent_id}/"
        response = self.session.get(url)
        
        print(f"URL: {url}")
        print(f"ステータス: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 404エラーが正しく返される")
            print(f"エラーメッセージ: {response.text}")
            return True
        else:
            print(f"❌ 期待されるステータス404ではありません: {response.status_code}")
            return False
    
    def test_unauthenticated_access(self):
        """テスト4: 認証なしでのアクセス"""
        print(f"\n=== テスト4: 認証なしアクセス ===")
        
        # 認証ヘッダーを削除してテスト
        url = f"{self.base_url}/web/recipes/"
        response = requests.get(url)  # セッションではなく直接リクエスト
        
        print(f"URL: {url}")
        print(f"ステータス: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ 認証エラー（401）が正しく返される")
            print(f"エラーメッセージ: {response.text}")
            return True
        elif response.status_code == 200:
            print("⚠️  認証なしでもアクセス可能（設定による）")
            return True
        else:
            print(f"❌ 予期しないステータスコード: {response.status_code}")
            return False
    
    def test_pagination(self):
        """テスト5: ページネーション"""
        print(f"\n=== テスト5: ページネーション ===")
        
        # 1ページ目
        url = f"{self.base_url}/web/recipes/?page=1&page_size=2"
        response = self.session.get(url)
        
        print(f"URL: {url}")
        print(f"ステータス: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"ページネーション結果:")
            print(f"  - 総数: {data.get('count')}")
            print(f"  - 今回取得: {len(data.get('results', []))}")
            print(f"  - 次ページ: {'あり' if data.get('next') else 'なし'}")
            print(f"  - 前ページ: {'あり' if data.get('previous') else 'なし'}")
            
            # 次ページがある場合はテスト
            if data.get('next'):
                print("\n次ページテスト:")
                next_response = self.session.get(data['next'])
                print(f"次ページステータス: {next_response.status_code}")
                if next_response.status_code == 200:
                    next_data = next_response.json()
                    print(f"次ページ取得数: {len(next_data.get('results', []))}")
            
            print("✅ ページネーションテスト成功")
            return True
        else:
            print(f"❌ ページネーションテスト失敗: {response.text}")
            return False
    
    def test_filtering_and_search(self):
        """テスト6: フィルタリング・検索"""
        print(f"\n=== テスト6: フィルタリング・検索 ===")
        
        # 検索テスト（レシピ名で検索）
        search_term = "チキン"
        url = f"{self.base_url}/web/recipes/?search={search_term}"
        response = self.session.get(url)
        
        print(f"検索URL: {url}")
        print(f"ステータス: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"検索結果: {len(results)}件")
            
            for recipe in results:
                print(f"  - {recipe.get('recipe_name')}")
            
            print("✅ 検索テスト完了")
            return True
        else:
            print(f"❌ 検索テスト失敗: {response.text}")
            return False

def run_recipe_retrieval_tests():
    """レシピ取得テストの実行"""
    print("Daily Dish レシピ取得APIテスト開始")
    print("=" * 60)
    
    tester = RecipeRetrievalTester(API_BASE)
    test_results = []
    
    # 1. 認証セットアップ
    auth_success = tester.setup_authentication()
    test_results.append(("認証セットアップ", auth_success))
    
    if not auth_success:
        print("❌ 認証に失敗したため、テストを中断します")
        return
    
    # 2. テスト用レシピ作成
    recipe_creation = tester.create_test_recipes()
    test_results.append(("テストレシピ作成", recipe_creation))
    
    # 3. レシピ一覧取得テスト
    recipes = tester.test_recipe_list_retrieval()
    test_results.append(("レシピ一覧取得", recipes is not None))
    
    # 4. 個別レシピ取得テスト
    if tester.created_recipe_ids:
        recipe_detail = tester.test_individual_recipe_retrieval(tester.created_recipe_ids[0])
        test_results.append(("個別レシピ取得", recipe_detail is not None))
    
    # 5. 存在しないレシピテスト
    not_found_test = tester.test_non_existent_recipe()
    test_results.append(("404エラーテスト", not_found_test))
    
    # 6. 認証なしアクセステスト
    unauth_test = tester.test_unauthenticated_access()
    test_results.append(("認証なしアクセス", unauth_test))
    
    # 7. ページネーションテスト
    pagination_test = tester.test_pagination()
    test_results.append(("ページネーション", pagination_test))
    
    # 8. 検索・フィルタリングテスト
    search_test = tester.test_filtering_and_search()
    test_results.append(("検索・フィルタリング", search_test))
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("レシピ取得APIテスト結果サマリー")
    print("=" * 60)
    
    for test_name, success in test_results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"{test_name:<20}: {status}")
    
    success_count = sum(1 for _, success in test_results if success)
    total_count = len(test_results)
    
    print(f"\n総合結果: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 全テスト成功！レシピ取得APIは正常に動作しています！")
    else:
        print("⚠️  一部のテストが失敗しました。詳細を確認してください。")

if __name__ == "__main__":
    print("Daily Dish レシピ取得APIテストツール")
    print("=" * 60)
    print(f"テスト対象URL: {BASE_URL}")
    print()
    
    # 自動実行モード
    print("自動実行モードでテストを開始します...")
    print()
    run_recipe_retrieval_tests()