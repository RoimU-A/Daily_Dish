#!/usr/bin/env python3
"""
食材キャッシュ複数削除API専用テスト
"""
import requests
import json

# Railway URL
BASE_URL = "https://web-production-889e.up.railway.app"
API_BASE = f"{BASE_URL}/api"

class IngredientBulkDeleteTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.created_ingredient_ids = []
    
    def setup_authentication(self):
        """認証のセットアップ"""
        print("=== 認証セットアップ ===")
        
        url = f"{self.base_url}/web/auth/login/"
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = requests.post(url, json=data)
        print(f"ログインステータス: {response.status_code}")
        
        if response.status_code == 200:
            self.access_token = response.json().get("access")
            print("✅ 認証成功")
            
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            })
            return True
        else:
            print(f"❌ 認証失敗: {response.text}")
            return False
    
    def create_test_ingredients(self):
        """テスト用食材キャッシュを作成"""
        print("\n=== テスト用食材キャッシュ作成 ===")
        
        test_ingredients = [
            {"ingredient_name": "玉ねぎ", "amount": 2.0, "unit": "個"},
            {"ingredient_name": "人参", "amount": 1.0, "unit": "本"},
            {"ingredient_name": "じゃがいも", "amount": 3.0, "unit": "個"},
            {"ingredient_name": "豚肉", "amount": 300.0, "unit": "g"},
            {"ingredient_name": "醤油", "amount": 2.0, "unit": "大さじ"}
        ]
        
        url = f"{self.base_url}/web/ingredient-cache/"
        
        for i, ingredient_data in enumerate(test_ingredients, 1):
            response = self.session.post(url, json=ingredient_data)
            print(f"食材{i} 作成: {response.status_code}")
            
            if response.status_code == 201:
                ingredient_id = response.json().get("id")
                self.created_ingredient_ids.append(ingredient_id)
                print(f"✅ 食材{i} 作成成功 (ID: {ingredient_id})")
            else:
                print(f"❌ 食材{i} 作成失敗: {response.text}")
        
        print(f"作成された食材ID: {self.created_ingredient_ids}")
        return len(self.created_ingredient_ids) > 0
    
    def get_current_ingredients(self):
        """現在の食材キャッシュ一覧を取得"""
        print("\n=== 現在の食材キャッシュ一覧 ===")
        
        url = f"{self.base_url}/web/ingredient-cache/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            ingredients = data.get('results', [])
            print(f"現在の食材数: {len(ingredients)}")
            
            for ingredient in ingredients:
                print(f"  - ID:{ingredient['id']} {ingredient['ingredient_name']} {ingredient['amount']}{ingredient['unit']}")
            
            return ingredients
        else:
            print(f"❌ 食材一覧取得失敗: {response.text}")
            return []
    
    def test_bulk_delete_valid_ids(self):
        """テスト1: 有効なIDでの複数削除"""
        print(f"\n=== テスト1: 有効なIDでの複数削除 ===")
        
        if len(self.created_ingredient_ids) < 3:
            print("❌ テスト用食材が不足しています")
            return False
        
        # 最初の3つの食材を削除
        delete_ids = self.created_ingredient_ids[:3]
        url = f"{self.base_url}/web/ingredient-cache/bulk-delete/"
        data = {"ids": delete_ids}
        
        print(f"削除対象ID: {delete_ids}")
        print(f"URL: {url}")
        print(f"データ: {json.dumps(data, indent=2)}")
        
        response = self.session.delete(url, json=data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 複数削除成功: {result.get('deleted_count')}件削除")
            return True
        else:
            print("❌ 複数削除失敗")
            return False
    
    def test_bulk_delete_invalid_ids(self):
        """テスト2: 無効なIDでの複数削除"""
        print(f"\n=== テスト2: 無効なIDでの複数削除 ===")
        
        # 存在しないIDを指定
        invalid_ids = [99999, 99998, 99997]
        url = f"{self.base_url}/web/ingredient-cache/bulk-delete/"
        data = {"ids": invalid_ids}
        
        print(f"無効なID: {invalid_ids}")
        
        response = self.session.delete(url, json=data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.text}")
        
        if response.status_code == 404:
            print("✅ 無効なIDで適切な404エラー")
            return True
        else:
            print("❌ 期待される404エラーが返されませんでした")
            return False
    
    def test_bulk_delete_empty_ids(self):
        """テスト3: 空のIDリストでの削除"""
        print(f"\n=== テスト3: 空のIDリストでの削除 ===")
        
        url = f"{self.base_url}/web/ingredient-cache/bulk-delete/"
        data = {"ids": []}
        
        response = self.session.delete(url, json=data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.text}")
        
        if response.status_code == 400:
            print("✅ 空のIDリストで適切な400エラー")
            return True
        else:
            print("❌ 期待される400エラーが返されませんでした")
            return False
    
    def test_bulk_delete_invalid_format(self):
        """テスト4: 不正なフォーマットでの削除"""
        print(f"\n=== テスト4: 不正なフォーマットでの削除 ===")
        
        url = f"{self.base_url}/web/ingredient-cache/bulk-delete/"
        data = {"ids": "invalid_format"}  # 文字列を送信
        
        response = self.session.delete(url, json=data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.text}")
        
        if response.status_code == 400:
            print("✅ 不正なフォーマットで適切な400エラー")
            return True
        else:
            print("❌ 期待される400エラーが返されませんでした")
            return False
    
    def test_remaining_ingredients(self):
        """テスト5: 残り食材の確認"""
        print(f"\n=== テスト5: 残り食材の確認 ===")
        
        remaining_ingredients = self.get_current_ingredients()
        remaining_ids = [ing['id'] for ing in remaining_ingredients]
        
        # 削除されなかった食材のIDを確認
        expected_remaining = self.created_ingredient_ids[3:]  # 最初の3つを削除したので残りは4番目以降
        
        print(f"期待される残りID: {expected_remaining}")
        print(f"実際の残りID: {remaining_ids}")
        
        # 残りの食材も削除（クリーンアップ）
        if remaining_ids:
            print("\n残りの食材をクリーンアップ...")
            url = f"{self.base_url}/web/ingredient-cache/bulk-delete/"
            data = {"ids": remaining_ids}
            
            response = self.session.delete(url, json=data)
            if response.status_code == 200:
                print("✅ クリーンアップ完了")
            else:
                print(f"⚠️ クリーンアップ失敗: {response.text}")
        
        return True

def run_ingredient_bulk_delete_tests():
    """食材キャッシュ複数削除テストの実行"""
    print("Daily Dish 食材キャッシュ複数削除APIテスト開始")
    print("=" * 60)
    
    tester = IngredientBulkDeleteTester(API_BASE)
    test_results = []
    
    # 1. 認証セットアップ
    auth_success = tester.setup_authentication()
    test_results.append(("認証セットアップ", auth_success))
    
    if not auth_success:
        print("❌ 認証に失敗したため、テストを中断します")
        return
    
    # 2. テスト用食材作成
    ingredient_creation = tester.create_test_ingredients()
    test_results.append(("テスト食材作成", ingredient_creation))
    
    if not ingredient_creation:
        print("❌ テスト用食材作成に失敗したため、テストを中断します")
        return
    
    # 3. 現在の食材一覧確認
    tester.get_current_ingredients()
    
    # 4. 有効なIDでの複数削除テスト
    valid_delete_test = tester.test_bulk_delete_valid_ids()
    test_results.append(("有効ID複数削除", valid_delete_test))
    
    # 5. 無効なIDでの複数削除テスト
    invalid_delete_test = tester.test_bulk_delete_invalid_ids()
    test_results.append(("無効ID複数削除", invalid_delete_test))
    
    # 6. 空のIDリストでの削除テスト
    empty_ids_test = tester.test_bulk_delete_empty_ids()
    test_results.append(("空IDリスト削除", empty_ids_test))
    
    # 7. 不正なフォーマットでの削除テスト
    invalid_format_test = tester.test_bulk_delete_invalid_format()
    test_results.append(("不正フォーマット削除", invalid_format_test))
    
    # 8. 残り食材の確認とクリーンアップ
    remaining_test = tester.test_remaining_ingredients()
    test_results.append(("残り食材確認", remaining_test))
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("食材キャッシュ複数削除APIテスト結果サマリー")
    print("=" * 60)
    
    for test_name, success in test_results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"{test_name:<20}: {status}")
    
    success_count = sum(1 for _, success in test_results if success)
    total_count = len(test_results)
    
    print(f"\n総合結果: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 全テスト成功！複数削除APIは正常に動作しています！")
    else:
        print("⚠️ 一部のテストが失敗しました。詳細を確認してください。")

if __name__ == "__main__":
    print("Daily Dish 食材キャッシュ複数削除APIテストツール")
    print("=" * 60)
    print(f"テスト対象URL: {BASE_URL}")
    print()
    
    run_ingredient_bulk_delete_tests()