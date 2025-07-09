#!/usr/bin/env python3
"""
ngrok本番環境でのHTTPリクエストテスト
"""

import requests
import json

# ngrok URLを自動取得
def get_ngrok_url():
    """ngrok URLを自動取得"""
    try:
        import subprocess
        result = subprocess.run(['curl', '-s', 'http://localhost:4040/api/tunnels'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if data['tunnels']:
                return data['tunnels'][0]['public_url']
    except:
        pass
    return None

NGROK_URL = get_ngrok_url()
if not NGROK_URL:
    print("❌ ngrok URLを自動取得できませんでした")
    print("ngrokが起動していることを確認してください")
    exit(1)

print(f"🌐 使用するngrok URL: {NGROK_URL}")
BASE_URL = NGROK_URL

# テストユーザー
TEST_USER = {
    "username": "testuser_v2",
    "password": "testpassword123"
}

def login():
    """JWT認証でログイン"""
    print("=== ログイン中 ===")
    
    url = f"{BASE_URL}/api/web/auth/login/"
    response = requests.post(url, json=TEST_USER)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['access']
        print(f"✅ ログイン成功")
        print(f"Access Token: {access_token[:50]}...")
        return access_token
    else:
        print(f"❌ ログイン失敗: {response.status_code}")
        print(response.text)
        return None

def register_existing_recipe(access_token):
    """既存レシピ登録"""
    print("\n=== 既存レシピ登録 ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_data = {
        "recipe_name": "クックパッドの親子丼",
        "recipe_url": "https://cookpad.com/recipe/12345",
        "ingredient_1": "鶏もも肉", "amount_1": 200.0, "unit_1": "g",
        "ingredient_2": "卵", "amount_2": 3.0, "unit_2": "個",
        "ingredient_3": "玉ねぎ", "amount_3": 0.5, "unit_3": "個",
        "ingredient_4": "だし汁", "amount_4": 200.0, "unit_4": "ml",
        "ingredient_5": "醤油", "amount_5": 30.0, "unit_5": "ml"
    }
    
    url = f"{BASE_URL}/api/web/recipes/"
    response = requests.post(url, json=recipe_data, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 既存レシピ登録成功")
        print(f"   レシピ名: {data['recipe_name']}")
        print(f"   URL: {data['recipe_url']}")
        print(f"   材料数: {len(data['ingredients'])}")
        print(f"   既存レシピ判定: {data['is_existing_recipe']}")
        return data['id']
    else:
        print(f"❌ 既存レシピ登録失敗: {response.status_code}")
        print(response.text)
        return None

def register_new_recipe(access_token):
    """新規レシピ登録"""
    print("\n=== 新規レシピ登録 ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_data = {
        "recipe_name": "おばあちゃんの肉じゃが",
        "ingredient_1": "じゃがいも", "amount_1": 4.0, "unit_1": "個",
        "ingredient_2": "豚バラ肉", "amount_2": 300.0, "unit_2": "g",
        "ingredient_3": "人参", "amount_3": 1.0, "unit_3": "本",
        "ingredient_4": "玉ねぎ", "amount_4": 1.0, "unit_4": "個",
        "ingredient_5": "しらたき", "amount_5": 1.0, "unit_5": "袋"
    }
    
    url = f"{BASE_URL}/api/web/recipes/"
    response = requests.post(url, json=recipe_data, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 新規レシピ登録成功")
        print(f"   レシピ名: {data['recipe_name']}")
        print(f"   URL: {data['recipe_url']}")  # None
        print(f"   材料数: {len(data['ingredients'])}")
        print(f"   新規レシピ判定: {data['is_new_recipe']}")
        return data['id']
    else:
        print(f"❌ 新規レシピ登録失敗: {response.status_code}")
        print(response.text)
        return None

def get_recipe_list(access_token):
    """レシピ一覧取得"""
    print("\n=== レシピ一覧取得 ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{BASE_URL}/api/web/recipes/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ レシピ一覧取得成功: {data['count']}件")
        for i, recipe in enumerate(data['results'], 1):
            url_info = f"URL: {recipe['recipe_url']}" if recipe['recipe_url'] else "新規レシピ"
            print(f"   {i}. {recipe['recipe_name']} ({url_info})")
    else:
        print(f"❌ レシピ一覧取得失敗: {response.status_code}")
        print(response.text)

def cook_recipe(access_token, recipe_id):
    """料理履歴登録"""
    if not recipe_id:
        print("\n⚠️ レシピIDがないため、料理履歴登録をスキップ")
        return
    
    print(f"\n=== 料理履歴登録（レシピID: {recipe_id}） ===")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    cook_data = {"recipe": recipe_id}
    
    url = f"{BASE_URL}/api/web/cooked-dishes/"
    response = requests.post(url, json=cook_data, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 料理履歴登録成功")
        print(f"   レシピ名: {data['recipe_detail']['recipe_name']}")
        print(f"   料理日時: {data['created_at']}")
    else:
        print(f"❌ 料理履歴登録失敗: {response.status_code}")
        print(response.text)

def main():
    """メイン処理"""
    print("Daily Dish ngrok本番環境 HTTPリクエストテスト")
    print("=" * 50)
    
    # 1. ログイン
    access_token = login()
    if not access_token:
        return
    
    # 2. 既存レシピ登録
    existing_recipe_id = register_existing_recipe(access_token)
    
    # 3. 新規レシピ登録
    new_recipe_id = register_new_recipe(access_token)
    
    # 4. レシピ一覧取得
    get_recipe_list(access_token)
    
    # 5. 料理履歴登録
    cook_recipe(access_token, existing_recipe_id or new_recipe_id)
    
    print("\n" + "=" * 50)
    print("テスト完了！")
    print("ngrokのWeb Interfaceでリクエスト詳細を確認できます:")
    print("http://localhost:4040")

if __name__ == "__main__":
    main()