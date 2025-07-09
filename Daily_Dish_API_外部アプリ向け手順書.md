# Daily Dish v2 API 外部アプリ向けリクエスト手順書

## 基本情報

### API Base URL
```
https://YOUR_NGROK_URL.ngrok.io
```
**現在のURL**: `https://82427e33d934.ngrok-free.app`

### 認証方式
- **Web API**: JWT認証（Bearer Token）
- **外部API**: API Key認証（X-API-KEY Header）

---

## 1. 認証・ユーザー管理

### 1.1 ユーザー登録

**エンドポイント**: `POST /api/web/auth/register/`  
**認証**: 不要

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123"
  }'
```

**レスポンス例**:
```json
{
  "id": 2,
  "username": "newuser",
  "email": "newuser@example.com",
  "created_at": "2025-07-09T20:15:00Z"
}
```

### 1.2 ログイン（JWT取得）

**エンドポイント**: `POST /api/web/auth/login/`  
**認証**: 不要

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser_v2",
    "password": "testpassword123"
  }'
```

**レスポンス例**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 1.3 ユーザープロフィール取得

**エンドポイント**: `GET /api/web/auth/profile/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 2. 統一レシピ管理

### 2.1 レシピ一覧取得

**エンドポイント**: `GET /api/web/recipes/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**レスポンス例**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "user": "testuser_v2",
      "recipe_name": "クックパッドの親子丼",
      "recipe_url": "https://cookpad.com/recipe/12345",
      "ingredients": [
        {"name": "鶏もも肉", "amount": 200.0, "unit": "g"},
        {"name": "卵", "amount": 3.0, "unit": "個"}
      ],
      "is_existing_recipe": true,
      "is_new_recipe": false,
      "created_at": "2025-07-09T20:03:00Z"
    }
  ]
}
```

### 2.2 既存レシピ登録

**エンドポイント**: `POST /api/web/recipes/`  
**認証**: JWT必須

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipe_name": "クックパッドの唐揚げ",
    "recipe_url": "https://cookpad.com/recipe/67890",
    "ingredient_1": "鶏もも肉",
    "amount_1": 300.0,
    "unit_1": "g",
    "ingredient_2": "醤油",
    "amount_2": 30.0,
    "unit_2": "ml",
    "ingredient_3": "にんにく",
    "amount_3": 1.0,
    "unit_3": "片"
  }'
```

### 2.3 新規レシピ登録

**エンドポイント**: `POST /api/web/recipes/`  
**認証**: JWT必須

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipe_name": "母の味噌汁",
    "ingredient_1": "だし汁",
    "amount_1": 400.0,
    "unit_1": "ml",
    "ingredient_2": "味噌",
    "amount_2": 30.0,
    "unit_2": "g",
    "ingredient_3": "わかめ",
    "amount_3": 10.0,
    "unit_3": "g"
  }'
```

### 2.4 レシピ詳細取得

**エンドポイント**: `GET /api/web/recipes/{id}/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2.5 レシピ更新

**エンドポイント**: `PUT /api/web/recipes/{id}/`  
**認証**: JWT必須

```bash
curl -X PUT https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipe_name": "クックパッドの親子丼（改良版）",
    "recipe_url": "https://cookpad.com/recipe/12345",
    "ingredient_1": "鶏もも肉",
    "amount_1": 250.0,
    "unit_1": "g"
  }'
```

### 2.6 レシピ削除

**エンドポイント**: `DELETE /api/web/recipes/{id}/`  
**認証**: JWT必須

```bash
curl -X DELETE https://YOUR_NGROK_URL.ngrok.io/api/web/recipes/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 3. 料理履歴管理

### 3.1 料理履歴一覧取得

**エンドポイント**: `GET /api/web/cooked-dishes/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/cooked-dishes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**レスポンス例**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "user": "testuser_v2",
      "recipe": 1,
      "recipe_detail": {
        "id": 1,
        "recipe_name": "クックパッドの親子丼",
        "recipe_url": "https://cookpad.com/recipe/12345",
        "ingredients": [...]
      },
      "created_at": "2025-07-09T20:03:00Z"
    }
  ]
}
```

### 3.2 料理履歴登録

**エンドポイント**: `POST /api/web/cooked-dishes/`  
**認証**: JWT必須

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/cooked-dishes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipe": 1
  }'
```

### 3.3 料理履歴削除

**エンドポイント**: `DELETE /api/web/cooked-dishes/{id}/`  
**認証**: JWT必須

```bash
curl -X DELETE https://YOUR_NGROK_URL.ngrok.io/api/web/cooked-dishes/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 4. 食材キャッシュ管理

### 4.1 食材キャッシュ一覧取得

**エンドポイント**: `GET /api/web/ingredient-cache/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/ingredient-cache/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4.2 食材キャッシュ登録

**エンドポイント**: `POST /api/web/ingredient-cache/`  
**認証**: JWT必須

```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/api/web/ingredient-cache/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "ingredient_name": "鶏肉",
    "amount": 500.0,
    "unit": "g"
  }'
```

### 4.3 食材キャッシュ削除

**エンドポイント**: `DELETE /api/web/ingredient-cache/{id}/`  
**認証**: JWT必須

```bash
curl -X DELETE https://YOUR_NGROK_URL.ngrok.io/api/web/ingredient-cache/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 5. 統計・分析

### 5.1 ユーザー統計情報

**エンドポイント**: `GET /api/web/stats/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**レスポンス例**:
```json
{
  "total_recipes": 5,
  "total_cooked_dishes": 3,
  "total_ingredient_cache": 0
}
```

### 5.2 ユーザーダッシュボード

**エンドポイント**: `GET /api/web/dashboard/`  
**認証**: JWT必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/web/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 6. 外部API（API Key認証）

### 6.1 システム統計情報

**エンドポイント**: `GET /api/external/stats/`  
**認証**: API Key必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/external/stats/ \
  -H "X-API-KEY: test-api-key-v2-12345"
```

**レスポンス例**:
```json
{
  "total_recipes": 10,
  "total_cooked_dishes": 15,
  "total_users": 3,
  "total_ingredient_cache": 5
}
```

### 6.2 全レシピ一覧（外部向け）

**エンドポイント**: `GET /api/external/recipes/`  
**認証**: API Key必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/external/recipes/ \
  -H "X-API-KEY: test-api-key-v2-12345"
```

### 6.3 全料理履歴（外部向け）

**エンドポイント**: `GET /api/external/cooked-dishes/`  
**認証**: API Key必須

```bash
curl -X GET https://YOUR_NGROK_URL.ngrok.io/api/external/cooked-dishes/ \
  -H "X-API-KEY: test-api-key-v2-12345"
```

---

## 7. エラーハンドリング

### 7.1 HTTPステータスコード

| コード | 説明 | 対応 |
|--------|------|------|
| 200 | 正常取得 | - |
| 201 | 正常作成 | - |
| 400 | リクエストエラー | リクエスト内容を確認 |
| 401 | 認証エラー | トークン・API Keyを確認 |
| 403 | 権限エラー | 所有者権限を確認 |
| 404 | リソース未存在 | IDを確認 |
| 500 | サーバーエラー | サーバー管理者に連絡 |

### 7.2 エラーレスポンス例

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力データに不正があります",
    "details": {
      "recipe_name": ["この項目は必須です"],
      "amount_1": ["正の数値を入力してください"]
    }
  }
}
```

---

## 8. 開発者向け情報

### 8.1 テスト用データ

**テストユーザー**:
- Username: `testuser_v2`
- Password: `testpassword123`
- Email: `testv2@example.com`

**テスト用API Key**:
- `test-api-key-v2-12345`

### 8.2 レート制限

**無料ngrok制限**:
- 同時接続数: 制限あり
- セッション時間: 8時間
- 帯域幅: 制限あり

### 8.3 デバッグ情報

**ngrok Web Interface**: `http://localhost:4040`
- リクエスト/レスポンス詳細
- エラーログ確認
- パフォーマンス監視

### 8.4 材料フィールド仕様

**材料登録形式**:
```json
{
  "ingredient_1": "材料名",
  "amount_1": 数値,
  "unit_1": "単位",
  "ingredient_2": "材料名2",
  "amount_2": 数値,
  "unit_2": "単位2"
}
```

**制限**:
- 材料数: 最大20個（ingredient_1～ingredient_20）
- 材料名: 最大100文字
- 単位: 最大20文字
- 分量: 小数点以下1桁まで

---

## 9. 使用例（Python）

### 9.1 基本的な使用フロー

```python
import requests

BASE_URL = "https://YOUR_NGROK_URL.ngrok.io"

# 1. ログイン
login_response = requests.post(f"{BASE_URL}/api/web/auth/login/", json={
    "username": "testuser_v2",
    "password": "testpassword123"
})
access_token = login_response.json()['access']

# 2. レシピ登録
headers = {"Authorization": f"Bearer {access_token}"}
recipe_data = {
    "recipe_name": "手作りカレー",
    "ingredient_1": "牛肉", "amount_1": 300.0, "unit_1": "g",
    "ingredient_2": "玉ねぎ", "amount_2": 2.0, "unit_2": "個"
}
recipe_response = requests.post(f"{BASE_URL}/api/web/recipes/", 
                               json=recipe_data, headers=headers)
recipe_id = recipe_response.json()['id']

# 3. 料理履歴登録
cook_response = requests.post(f"{BASE_URL}/api/web/cooked-dishes/", 
                             json={"recipe": recipe_id}, headers=headers)
```

---

## 10. サポート・お問い合わせ

**技術サポート**:
- ngrok起動確認: `./ngrok version`
- サーバー状態確認: `ps aux | grep python`
- ログ確認: `tail -f django_production.log`

**問題発生時の対応**:
1. ngrokの再起動
2. Djangoサーバーの再起動
3. トークンの再取得
4. API Keyの確認

---

*この手順書は Daily Dish v2 統一レシピ管理システム用です。*  
*最終更新: 2025年7月9日*