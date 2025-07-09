# Daily Dish データベース移行ガイド

## 移行概要

SQLiteからRailway PostgreSQLへのデータ移行手順

## 事前準備

### 1. 現在のデータ確認
```bash
# 現在のデータを確認
python check_db_state.py
```

### 2. データバックアップ
```bash
# SQLiteデータベースのバックアップ
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

## 移行手順

### オプション1: 新規セットアップ（推奨）

#### Railway デプロイ後
1. **マイグレーション実行**
   ```bash
   # Railway Console で実行
   python manage.py migrate
   ```

2. **スーパーユーザー作成**
   ```bash
   python manage.py createsuperuser
   ```

3. **API Key作成**
   ```bash
   python create_api_key.py
   ```

4. **テストデータ投入（オプション）**
   ```bash
   python sample_data_test.py
   ```

### オプション2: 既存データ移行

#### ステップ1: データエクスポート
```bash
# ローカルでデータをJSON形式でエクスポート
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission -e auth.Group \
  --indent 2 > daily_dish_data.json
```

#### ステップ2: データ検証
```bash
# エクスポートデータの確認
python -m json.tool daily_dish_data.json > /dev/null
echo "JSONデータは有効です"
```

#### ステップ3: Railway環境でデータインポート
```bash
# Railway Console で実行

# 1. マイグレーション実行
python manage.py migrate

# 2. データインポート
python manage.py loaddata daily_dish_data.json

# 3. スーパーユーザー作成（必要に応じて）
python manage.py createsuperuser
```

## データ移行スクリプト

### 自動移行スクリプト作成
```python
# migrate_to_railway.py
import os
import subprocess
import json

def export_data():
    """SQLiteからデータをエクスポート"""
    print("データをエクスポート中...")
    cmd = [
        'python', 'manage.py', 'dumpdata',
        '--natural-foreign', '--natural-primary',
        '-e', 'contenttypes', '-e', 'auth.Permission',
        '-e', 'auth.Group', '--indent', '2'
    ]
    
    with open('daily_dish_data.json', 'w') as f:
        subprocess.run(cmd, stdout=f, check=True)
    
    print("データエクスポート完了: daily_dish_data.json")

def validate_json():
    """JSONデータの有効性確認"""
    print("JSONデータを検証中...")
    try:
        with open('daily_dish_data.json', 'r') as f:
            json.load(f)
        print("✅ JSONデータは有効です")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSONエラー: {e}")
        return False

def show_data_summary():
    """データサマリー表示"""
    print("データサマリー:")
    with open('daily_dish_data.json', 'r') as f:
        data = json.load(f)
    
    models = {}
    for item in data:
        model = item['model']
        models[model] = models.get(model, 0) + 1
    
    for model, count in models.items():
        print(f"  {model}: {count} レコード")

if __name__ == '__main__':
    export_data()
    if validate_json():
        show_data_summary()
        print("\n次の手順:")
        print("1. daily_dish_data.json をRailwayプロジェクトにアップロード")
        print("2. Railway Console で: python manage.py loaddata daily_dish_data.json")
```

## 移行後の確認

### 1. データ整合性確認
```bash
# レコード数確認
python manage.py shell << EOF
from daily_dish.models import *
print(f"Users: {User.objects.count()}")
print(f"Recipes: {Recipe.objects.count()}")
print(f"CookedDishes: {CookedDish.objects.count()}")
print(f"IngredientCache: {IngredientCache.objects.count()}")
print(f"ApiKeys: {ApiKey.objects.count()}")
EOF
```

### 2. API動作確認
```bash
# 統計API確認
curl -X GET "https://your-app.up.railway.app/api/external/stats/" \
  -H "X-API-KEY: your-api-key"
```

### 3. 認証機能確認
```bash
# JWT認証確認
curl -X POST "https://your-app.up.railway.app/api/web/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "your-username", "password": "your-password"}'
```

## トラブルシューティング

### 問題1: 外部キー制約エラー
**解決策**: 
```bash
# データを順序立てて投入
python manage.py loaddata --ignorenonexistent daily_dish_data.json
```

### 問題2: ユニーク制約エラー
**解決策**:
```bash
# 既存データを確認・削除
python manage.py flush
python manage.py loaddata daily_dish_data.json
```

### 問題3: エンコーディングエラー
**解決策**:
```bash
# UTF-8で再エクスポート
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission -e auth.Group \
  --indent 2 --output daily_dish_data.json
```

## 最終確認チェックリスト

- [ ] マイグレーション実行完了
- [ ] スーパーユーザー作成完了
- [ ] API Key作成完了
- [ ] 全モデルのデータ移行完了
- [ ] JWT認証動作確認
- [ ] API Key認証動作確認
- [ ] 統計API動作確認
- [ ] レシピCRUD動作確認
- [ ] 料理履歴機能動作確認

## バックアップとリカバリ

### 定期バックアップ設定
```bash
# crontabで自動バックアップ（Railway Console）
0 2 * * * python manage.py dumpdata > backup_$(date +\%Y\%m\%d).json
```

### 緊急時リカバリ
```bash
# バックアップからリストア
python manage.py flush
python manage.py loaddata backup_YYYYMMDD.json
```