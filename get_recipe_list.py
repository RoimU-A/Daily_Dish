#!/usr/bin/env python3
"""
レシピ一覧取得専用スクリプト
"""

import requests
import json
import subprocess

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

def login(base_url):
    """JWT認証でログイン"""
    print("🔐 ログイン中...")
    
    url = f"{base_url}/api/web/auth/login/"
    user_data = {
        "username": "testuser_v2",
        "password": "testpassword123"
    }
    
    response = requests.post(url, json=user_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ ログイン成功")
        return data['access']
    else:
        print(f"❌ ログイン失敗: {response.status_code}")
        print(response.text)
        return None

def get_recipe_list(base_url, access_token):
    """レシピ一覧を取得"""
    print("\n📋 レシピ一覧を取得中...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{base_url}/api/web/recipes/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ レシピ一覧取得成功: {data['count']}件")
        print("=" * 60)
        
        if data['count'] == 0:
            print("📝 登録されているレシピはありません")
            return
        
        for i, recipe in enumerate(data['results'], 1):
            print(f"\n【レシピ {i}】")
            print(f"   📌 名前: {recipe['recipe_name']}")
            print(f"   🆔 ID: {recipe['id']}")
            
            if recipe['recipe_url']:
                print(f"   🌐 URL: {recipe['recipe_url']}")
                print(f"   📂 種別: 既存レシピ")
            else:
                print(f"   🌐 URL: なし")
                print(f"   📂 種別: 新規レシピ")
            
            print(f"   📅 作成日: {recipe['created_at'][:10]}")
            
            # 材料リスト表示
            ingredients = recipe['ingredients']
            if ingredients:
                print(f"   🥘 材料 ({len(ingredients)}種類):")
                for j, ingredient in enumerate(ingredients, 1):
                    print(f"      {j}. {ingredient['name']} {ingredient['amount']}{ingredient['unit']}")
            else:
                print(f"   🥘 材料: 登録なし")
        
        print("\n" + "=" * 60)
        
        # サマリー表示
        existing_count = sum(1 for r in data['results'] if r['recipe_url'])
        new_count = data['count'] - existing_count
        print(f"📊 サマリー:")
        print(f"   既存レシピ: {existing_count}件")
        print(f"   新規レシピ: {new_count}件")
        print(f"   合計: {data['count']}件")
        
        return data['results']
    else:
        print(f"❌ レシピ一覧取得失敗: {response.status_code}")
        print(response.text)
        return None

def main():
    """メイン処理"""
    print("Daily Dish レシピ一覧取得")
    print("=" * 30)
    
    # 1. ngrok URL取得
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        print("❌ ngrok URLを取得できませんでした")
        print("ngrokが起動していることを確認してください")
        return
    
    print(f"🌐 ngrok URL: {ngrok_url}")
    
    # 2. ログイン
    access_token = login(ngrok_url)
    if not access_token:
        return
    
    # 3. レシピ一覧取得
    recipes = get_recipe_list(ngrok_url, access_token)
    
    if recipes is not None:
        print(f"\n🎉 レシピ一覧取得完了！")
    
    print(f"\n💡 Web Interfaceでリクエスト詳細確認: http://localhost:4040")

if __name__ == "__main__":
    main()