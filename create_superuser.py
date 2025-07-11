#!/usr/bin/env python
"""
一時的なスーパーユーザー作成スクリプト
Railway環境で一度だけ実行
"""
import os
import django

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_dish_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# スーパーユーザーが存在しない場合のみ作成
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@daily-dish.com',
        password='admin123456'  # 実際の運用では変更してください
    )
    print("✅ スーパーユーザー 'admin' を作成しました")
    print("Username: admin")
    print("Password: admin123456")
    print("⚠️  ログイン後、パスワードを変更してください")
else:
    print("✅ スーパーユーザーは既に存在します")