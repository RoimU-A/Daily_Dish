#!/usr/bin/env python3
"""
API エラー詳細確認用スクリプト
"""
import requests
import json

BASE_URL = "https://web-production-889e.up.railway.app"

def debug_user_registration():
    """ユーザー登録のデバッグ"""
    print("=== ユーザー登録エラー詳細確認 ===")
    
    url = f"{BASE_URL}/api/web/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword123"
    }
    
    print(f"リクエストURL: {url}")
    print(f"リクエストデータ: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンスヘッダー: {dict(response.headers)}")
        print(f"レスポンス内容: {response.text}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_data = response.json()
                print(f"JSON データ: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
            except:
                print("JSON パースエラー")
                
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")

def check_endpoints():
    """エンドポイント存在確認"""
    print("\n=== エンドポイント確認 ===")
    
    endpoints = [
        "/api/",
        "/api/web/",
        "/api/web/auth/",
        "/api/web/auth/register/",
        "/admin/"
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            print(f"{endpoint}: {response.status_code} - {response.reason}")
        except Exception as e:
            print(f"{endpoint}: エラー - {e}")

def check_csrf_requirement():
    """CSRF要件確認"""
    print("\n=== CSRF要件確認 ===")
    
    # GETでCSRFトークン取得を試行
    try:
        response = requests.get(f"{BASE_URL}/api/web/auth/register/")
        print(f"GET /register/: {response.status_code}")
        print(f"Set-Cookie: {response.headers.get('Set-Cookie', 'なし')}")
    except Exception as e:
        print(f"CSRF確認エラー: {e}")

if __name__ == "__main__":
    debug_user_registration()
    check_endpoints()
    check_csrf_requirement()