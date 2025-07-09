# Daily Dish API テストガイド

このガイドでは、実装されたAPIをテストする方法を説明します。

## 前提条件

1. Django開発サーバーが起動していること
2. 必要なパッケージがインストールされていること

## 1. サーバー起動

```bash
# Django開発サーバーを起動
python manage.py runserver

# サーバーが http://localhost:8000 で起動します
```

## 2. API Key作成（外部APIテスト用）

外部APIをテストするには、事前にAPI Keyを作成する必要があります。

```bash
# API Key作成スクリプトを実行
python create_api_key.py
```

## 3. テスト方法

### 方法1: Pythonスクリプトによるテスト

```bash
# requestsライブラリをインストール（未インストールの場合）
pip install requests

# テストスクリプトを実行
python test_api_examples.py
```

**実行内容:**
- ユーザー登録
- ログイン（JWT取得）
- レシピCRUD操作
- 登録済みレシピ管理
- 料理履歴作成
- ダッシュボード取得
- 外部API統計情報

### 方法2: curlコマンドによるテスト

```bash
# jqツールがあると見やすくなります（オプション）
# Ubuntu/Debian: sudo apt-get install jq
# macOS: brew install jq

# curlテストスクリプトを実行
bash curl_examples.sh
```

**個別のcurlコマンド例:**

```bash
# 1. ユーザー登録
curl -X POST "http://localhost:8000/api/web/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123", 
    "password_confirm": "testpassword123"
  }'

# 2. ログイン
curl -X POST "http://localhost:8000/api/web/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'

# 3. レシピ作成（要JWT）
curl -X POST "http://localhost:8000/api/web/recipes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipe_name": "親子丼",
    "ingredient_1": "鶏肉",
    "amount_1": "300.0",
    "unit_1": "g"
  }'

# 4. 外部API統計（要API Key）
curl -X GET "http://localhost:8000/api/external/stats/" \
  -H "X-API-KEY: test-key-12345"
```

### 方法3: Postmanによるテスト

1. Postmanアプリを開く
2. `Daily_Dish_API.postman_collection.json` をインポート
3. 環境変数を設定:
   - `BASE_URL`: `http://localhost:8000`
   - `API_KEY`: `test-key-12345`
4. コレクション内のリクエストを順番に実行

## 4. API エンドポイント一覧

### Web API (JWT認証)

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/api/web/auth/register/` | POST | ユーザー登録 |
| `/api/web/auth/login/` | POST | ログイン |
| `/api/web/auth/profile/` | GET/PUT | プロフィール |
| `/api/web/recipes/` | GET/POST | レシピ一覧・作成 |
| `/api/web/recipes/{id}/` | GET/PUT/DELETE | レシピ詳細 |
| `/api/web/registered-recipes/` | GET/POST | 登録済みレシピ |
| `/api/web/cooked-dishes/` | GET/POST | 料理履歴 |
| `/api/web/ingredient-cache/` | GET/POST | 食材キャッシュ |
| `/api/web/dashboard/` | GET | ダッシュボード |

### 外部API (API Key認証)

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/api/external/stats/` | GET | 統計情報 |
| `/api/external/recipes/` | GET | レシピ一覧 |
| `/api/external/recent-activities/` | GET | 最近のアクティビティ |

## 5. 認証について

### JWT認証（Web API）
- ログイン時にaccess_tokenとrefresh_tokenを取得
- APIリクエスト時に `Authorization: Bearer {access_token}` ヘッダーを付与

### API Key認証（外部API）
- 事前に作成したAPI Keyを使用
- APIリクエスト時に `X-API-KEY: {api_key}` ヘッダーを付与

## 6. レスポンス例

### ログイン成功レスポンス
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### レシピ作成レスポンス
```json
{
  "id": 1,
  "user": "testuser",
  "recipe_name": "親子丼",
  "ingredients": [
    {"name": "鶏肉", "amount": 300.0, "unit": "g"},
    {"name": "玉ねぎ", "amount": 1.0, "unit": "個"}
  ],
  "created_at": "2025-07-09T12:00:00Z"
}
```

### ダッシュボードレスポンス
```json
{
  "stats": {
    "total_recipes": 5,
    "total_registered_recipes": 3,
    "total_cooked_dishes": 8
  },
  "recent_activities": [...],
  "user_info": {...}
}
```

## 7. トラブルシューティング

### 401 Unauthorized
- JWT: アクセストークンが無効または期限切れ
- API Key: API Keyが無効または存在しない

### 403 Forbidden
- 他のユーザーのリソースにアクセスしようとしている

### 404 Not Found
- 存在しないリソースIDを指定している
- 自分のリソースでないものにアクセスしている

### 400 Bad Request
- リクエストボディの形式が間違っている
- 必須フィールドが不足している
- バリデーションエラー

## 8. 自動テストの実行

```bash
# 全テスト実行
python manage.py test

# APIテストのみ実行
python manage.py test daily_dish.test_api

# モデルテストのみ実行
python manage.py test daily_dish.tests
```

## まとめ

Daily Dish APIは以下の機能を提供します：
- ユーザー認証とプロフィール管理
- レシピの作成・管理
- 料理履歴の記録
- 食材キャッシュの管理
- 統計情報とダッシュボード
- 外部アプリ向けデータ提供

各APIは適切な認証とアクセス制御により保護されており、ユーザーは自分のデータのみアクセス可能です。