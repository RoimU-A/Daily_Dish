#!/usr/bin/env python3
"""
食材キャッシュ複数削除API簡易テスト
新しいユーザーを作成してテストを実行
"""
import requests
import json
import random
import string

BASE_URL = "https://web-production-889e.up.railway.app"
API_BASE = f"{BASE_URL}/api"

def generate_random_username():
    """ランダムなユーザー名を生成"""
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"testuser_{suffix}"

def create_test_user_and_login():
    """テストユーザーを作成してログイン"""
    username = generate_random_username()
    password = "testpassword123"
    email = f"{username}@example.com"
    
    print(f"=== テストユーザー作成: {username} ===")
    
    # ユーザー登録
    register_url = f"{API_BASE}/web/auth/register/"
    register_data = {
        "username": username,
        "email": email,
        "password": password,
        "password_confirm": password
    }
    
    register_response = requests.post(register_url, json=register_data)
    print(f"ユーザー登録ステータス: {register_response.status_code}")
    
    if register_response.status_code != 201:
        print(f"❌ ユーザー登録失敗: {register_response.text}")
        return None, None
    
    print("✅ ユーザー登録成功")
    
    # ログイン
    login_url = f"{API_BASE}/web/auth/login/"
    login_data = {
        "username": username,
        "password": password
    }
    
    login_response = requests.post(login_url, json=login_data)
    print(f"ログインステータス: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"❌ ログイン失敗: {login_response.text}")
        return None, None
    
    access_token = login_response.json().get("access")
    print("✅ ログイン成功")
    
    return username, access_token

def create_test_ingredients(session):
    """テスト用食材を作成"""
    print("\n=== テスト用食材作成 ===")
    
    ingredients = [
        {"ingredient_name": "テスト玉ねぎ", "amount": 2.0, "unit": "個"},
        {"ingredient_name": "テスト人参", "amount": 1.0, "unit": "本"},
        {"ingredient_name": "テストじゃがいも", "amount": 3.0, "unit": "個"},
        {"ingredient_name": "テスト豚肉", "amount": 300.0, "unit": "g"},
        {"ingredient_name": "テスト醤油", "amount": 2.0, "unit": "大さじ"}
    ]
    
    url = f"{API_BASE}/web/ingredient-cache/"
    created_ids = []
    
    for ingredient in ingredients:
        response = session.post(url, json=ingredient)
        if response.status_code == 201:
            ingredient_id = response.json().get("id")
            created_ids.append(ingredient_id)
            print(f"✅ {ingredient['ingredient_name']} 作成成功 (ID: {ingredient_id})")
        else:
            print(f"❌ {ingredient['ingredient_name']} 作成失敗: {response.text}")
    
    return created_ids

def test_bulk_delete(session, ids_to_delete):
    """複数削除APIのテスト"""
    print(f"\n=== 複数削除APIテスト ===")
    print(f"削除対象ID: {ids_to_delete}")
    
    url = f"{API_BASE}/web/ingredient-cache/bulk-delete/"
    data = {"ids": ids_to_delete}
    
    response = session.delete(url, json=data)
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 複数削除成功: {result.get('deleted_count')}件削除")
        return True
    else:
        print("❌ 複数削除失敗")
        return False

def get_ingredients_list(session):
    """食材一覧を取得"""
    url = f"{API_BASE}/web/ingredient-cache/"
    response = session.get(url)
    
    if response.status_code == 200:
        data = response.json()
        ingredients = data.get('results', [])
        print(f"\n現在の食材数: {len(ingredients)}")
        for ingredient in ingredients:
            print(f"  - ID:{ingredient['id']} {ingredient['ingredient_name']} {ingredient['amount']}{ingredient['unit']}")
        return ingredients
    else:
        print(f"❌ 食材一覧取得失敗: {response.text}")
        return []

def main():
    print("Daily Dish 食材キャッシュ複数削除API簡易テスト")
    print("=" * 60)
    
    # 1. テストユーザー作成・ログイン
    username, access_token = create_test_user_and_login()
    if not access_token:
        print("❌ 認証に失敗しました")
        return
    
    # セッション設定
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    })
    
    # 2. テスト用食材作成
    created_ids = create_test_ingredients(session)
    if not created_ids:
        print("❌ テスト用食材作成に失敗しました")
        return
    
    # 3. 作成後の食材一覧表示
    print("\n=== 作成後の食材一覧 ===")
    get_ingredients_list(session)
    
    # 4. 複数削除テスト（最初の3つを削除）
    if len(created_ids) >= 3:
        delete_ids = created_ids[:3]
        test_bulk_delete(session, delete_ids)
        
        # 5. 削除後の食材一覧表示
        print("\n=== 削除後の食材一覧 ===")
        remaining_ingredients = get_ingredients_list(session)
        
        # 6. 残りの食材もクリーンアップ
        if remaining_ingredients:
            print("\n=== 残り食材のクリーンアップ ===")
            remaining_ids = [ing['id'] for ing in remaining_ingredients]
            test_bulk_delete(session, remaining_ids)
            
            # 7. 最終確認
            print("\n=== 最終確認 ===")
            get_ingredients_list(session)
    
    print("\n🎉 テスト完了！")

if __name__ == "__main__":
    main()