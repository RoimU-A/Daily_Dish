#!/usr/bin/env python3
"""
特定エンドポイントの詳細テスト
"""
import requests
import json

BASE_URL = "https://web-production-889e.up.railway.app"

def test_user_registration_detailed():
    """ユーザー登録の詳細テスト"""
    print("=== ユーザー登録詳細テスト ===")
    
    # 1. CSRFトークン取得を試行
    print("1. CSRF トークン取得テスト")
    try:
        csrf_response = requests.get(f"{BASE_URL}/api/web/auth/register/")
        print(f"GET Status: {csrf_response.status_code}")
        print(f"GET Headers: {csrf_response.headers}")
        print(f"GET Content: {csrf_response.text[:200]}")
    except Exception as e:
        print(f"CSRF取得エラー: {e}")
    
    # 2. POST リクエスト（JSONヘッダー明示）
    print("\n2. POST リクエストテスト")
    url = f"{BASE_URL}/api/web/auth/register/"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "username": "testuser2",
        "email": "test2@example.com", 
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        print(f"POST Status: {response.status_code}")
        print(f"POST Headers: {response.headers}")
        print(f"POST Content: {response.text}")
        
        if response.status_code == 201:
            print("✅ ユーザー登録成功")
        else:
            print("❌ ユーザー登録失敗")
            
    except Exception as e:
        print(f"POST エラー: {e}")

def test_other_endpoints():
    """他のエンドポイントテスト"""
    print("\n=== 他エンドポイントテスト ===")
    
    endpoints = [
        ("基本API", "/api/"),
        ("外部統計", "/api/external/stats/"),
        ("Admin", "/admin/"),
    ]
    
    for name, endpoint in endpoints:
        print(f"\n{name}: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Content: {response.text[:100]}...")
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    test_user_registration_detailed()
    test_other_endpoints()