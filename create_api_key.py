#!/usr/bin/env python3
"""
API Key作成用スクリプト

外部APIテストのためのAPI Keyを作成します
"""

import os
import sys
import django

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_dish_project.settings')
django.setup()

from daily_dish.models import ApiKey

def create_test_api_key():
    """テスト用API Keyを作成"""
    api_key_value = "test-key-12345"
    
    # 既存のキーがあるかチェック
    existing_key = ApiKey.objects.filter(api_key=api_key_value).first()
    if existing_key:
        print(f"API Key '{api_key_value}' は既に存在します")
        print(f"Key Name: {existing_key.key_name}")
        print(f"Active: {existing_key.is_active}")
        return existing_key
    
    # 新しいAPI Keyを作成
    api_key = ApiKey.objects.create(
        key_name="テスト用API Key",
        api_key=api_key_value,
        is_active=True
    )
    
    print("✅ テスト用API Keyを作成しました")
    print(f"Key Name: {api_key.key_name}")
    print(f"API Key: {api_key.api_key}")
    print(f"Active: {api_key.is_active}")
    
    return api_key

def list_api_keys():
    """全API Keyを一覧表示"""
    api_keys = ApiKey.objects.all()
    
    if not api_keys:
        print("API Keyが登録されていません")
        return
    
    print("=== 登録済みAPI Key一覧 ===")
    for key in api_keys:
        status = "🟢 Active" if key.is_active else "🔴 Inactive"
        print(f"- {key.key_name}: {key.api_key} ({status})")
        print(f"  作成日時: {key.created_at}")
        print(f"  使用回数: {key.usage_count}")
        if key.last_used_at:
            print(f"  最終使用: {key.last_used_at}")
        print()

if __name__ == "__main__":
    print("Daily Dish API Key管理")
    print("=" * 30)
    
    # 既存のAPI Key一覧表示
    list_api_keys()
    
    # テスト用API Key作成
    create_test_api_key()
    
    print("\n" + "=" * 30)
    print("使用方法:")
    print("curlテスト: bash curl_examples.sh")
    print("Pythonテスト: python test_api_examples.py")
    print("PostmanでのテストにはAPI_KEY環境変数を 'test-key-12345' に設定してください")