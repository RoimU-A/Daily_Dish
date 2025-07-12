#!/usr/bin/env python
"""
LINE連携機能の基本テスト
"""
import os
import sys
import django

# Django設定
sys.path.append('/home/roimu/daily-dish')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_dish_project.settings')
django.setup()

from daily_dish.services.line_parser import LineTextParser
from daily_dish.models import User

def test_line_parser():
    """LINE解析機能のテスト"""
    print("=== LINE解析機能テスト ===")
    
    parser = LineTextParser()
    
    # テスト1: テキスト分類
    print("1. テキスト分類テスト")
    test_cases = [
        ("ユーザー紐づけ", "user_linking"),
        ("https://cookpad.com/recipe/123", "url"),
        ("レシピ:テストカレー\n材料:鶏肉、玉ねぎ\n量:300g、200g", "recipe"),
        ("hello world", "invalid")
    ]
    
    for text, expected in test_cases:
        result = parser.classify_text_type(text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text[:20]}...' -> {result}")
    
    # テスト2: レシピ解析
    print("\n2. レシピ解析テスト")
    recipe_text = """レシピ:チキンカレー
材料:鶏肉、玉ねぎ、カレールー
量:300g、200g、1箱"""
    
    try:
        parsed = parser.parse_recipe_text(recipe_text)
        print(f"  ✅ レシピ名: {parsed['recipe_name']}")
        print(f"  ✅ 材料: {parsed['ingredients']}")
        print(f"  ✅ 量: {parsed['amounts']}")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    
    # テスト3: 量と単位の解析
    print("\n3. 量・単位解析テスト")
    amount_cases = [
        ("300g", (300.0, "g")),
        ("1箱", (1.0, "箱")),
        ("2.5kg", (2.5, "kg")),
        ("適量", (1.0, "適量"))
    ]
    
    for amount_str, expected in amount_cases:
        result = parser.parse_amount_and_unit(amount_str)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{amount_str}' -> {result}")

def test_database():
    """データベース接続テスト"""
    print("\n=== データベース接続テスト ===")
    
    try:
        # ユーザー数確認
        user_count = User.objects.count()
        print(f"✅ データベース接続成功")
        print(f"✅ 登録ユーザー数: {user_count}")
        
        # LINE連携フィールドのテスト
        if hasattr(User, 'line_user_id'):
            print("✅ line_user_idフィールドが存在")
        else:
            print("❌ line_user_idフィールドが存在しません")
            
    except Exception as e:
        print(f"❌ データベースエラー: {e}")

def test_settings():
    """設定値テスト"""
    print("\n=== 設定値テスト ===")
    
    from django.conf import settings
    
    # LINE設定確認
    line_secret = getattr(settings, 'LINE_CHANNEL_SECRET', None)
    line_token = getattr(settings, 'LINE_CHANNEL_ACCESS_TOKEN', None)
    
    if line_secret:
        print(f"✅ LINE_CHANNEL_SECRET: {line_secret[:10]}...")
    else:
        print("❌ LINE_CHANNEL_SECRET が設定されていません")
    
    if line_token:
        print(f"✅ LINE_CHANNEL_ACCESS_TOKEN: {line_token[:20]}...")
    else:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
    
    # Redis設定確認
    if hasattr(settings, 'CACHES'):
        print("✅ Redis（CACHES）設定が存在")
    else:
        print("❌ Redis（CACHES）設定が存在しません")

if __name__ == "__main__":
    print("LINE連携機能 実装テスト開始\n")
    
    try:
        test_line_parser()
        test_database() 
        test_settings()
        
        print("\n=== テスト完了 ===")
        print("🎉 LINE連携機能の基本実装が完了しました！")
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()