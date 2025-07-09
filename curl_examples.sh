#!/bin/bash

# Daily Dish API テスト用 curl コマンド集
# 
# 使用方法:
# 1. Django開発サーバーを起動: python manage.py runserver
# 2. このスクリプトを実行: bash curl_examples.sh
#    または個別のコマンドをコピーして実行

BASE_URL="http://localhost:8000"

echo "=== Daily Dish API テスト ==="
echo "ベースURL: $BASE_URL"
echo

# 1. ユーザー登録
echo "1. ユーザー登録"
curl -X POST "$BASE_URL/api/web/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpassword123",
    "password_confirm": "testpassword123"
  }' | jq .

echo -e "\n"

# 2. ログイン（JWT トークン取得）
echo "2. ログイン"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/web/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }')

echo $LOGIN_RESPONSE | jq .

# JWTトークンを抽出
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r .access)
echo "取得したアクセストークン: $ACCESS_TOKEN"
echo

# 3. プロフィール取得
echo "3. ユーザープロフィール取得"
curl -X GET "$BASE_URL/api/web/auth/profile/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo -e "\n"

# 4. レシピ作成
echo "4. レシピ作成"
RECIPE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/web/recipes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "recipe_name": "親子丼",
    "ingredient_1": "鶏肉",
    "amount_1": "300.0",
    "unit_1": "g",
    "ingredient_2": "玉ねぎ",
    "amount_2": "1.0",
    "unit_2": "個",
    "ingredient_3": "卵",
    "amount_3": "3.0",
    "unit_3": "個"
  }')

echo $RECIPE_RESPONSE | jq .

# レシピIDを抽出
RECIPE_ID=$(echo $RECIPE_RESPONSE | jq -r .id)
echo "作成されたレシピID: $RECIPE_ID"
echo

# 5. レシピ一覧取得
echo "5. レシピ一覧取得"
curl -X GET "$BASE_URL/api/web/recipes/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo -e "\n"

# 6. レシピ詳細取得
echo "6. レシピ詳細取得"
curl -X GET "$BASE_URL/api/web/recipes/$RECIPE_ID/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo -e "\n"

# 7. 既存レシピ登録
echo "7. 既存レシピ登録"
curl -X POST "$BASE_URL/api/web/registered-recipes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "recipe_name": "クックパッドの唐揚げ",
    "recipe_type": "existing",
    "recipe_url": "https://cookpad.com/recipe/123456"
  }' | jq .

echo -e "\n"

# 8. 新規レシピ登録
echo "8. 新規レシピ登録"
REGISTERED_RESPONSE=$(curl -s -X POST "$BASE_URL/api/web/registered-recipes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"recipe_name\": \"親子丼\",
    \"recipe_type\": \"new\",
    \"recipe\": $RECIPE_ID
  }")

echo $REGISTERED_RESPONSE | jq .

# 登録済みレシピIDを抽出
REGISTERED_ID=$(echo $REGISTERED_RESPONSE | jq -r .id)
echo "登録済みレシピID: $REGISTERED_ID"
echo

# 9. 料理履歴作成
echo "9. 料理履歴作成"
curl -X POST "$BASE_URL/api/web/cooked-dishes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"registered_recipe\": $REGISTERED_ID
  }" | jq .

echo -e "\n"

# 10. ダッシュボード取得
echo "10. ダッシュボード取得"
curl -X GET "$BASE_URL/api/web/dashboard/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo -e "\n"

# 11. 食材キャッシュ作成
echo "11. 食材キャッシュ作成"
curl -X POST "$BASE_URL/api/web/ingredient-cache/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "ingredient_name": "鶏肉",
    "amount": "500.0",
    "unit": "g"
  }' | jq .

echo -e "\n"

echo "=== 外部API テスト（API Key が必要） ==="
echo "事前にAPI Keyを作成してください："
echo "python manage.py shell"
echo "from daily_dish.models import ApiKey"
echo "ApiKey.objects.create(key_name='テスト用', api_key='test-key-12345')"
echo

# 12. 外部API統計情報（API Key必要）
echo "12. 外部API統計情報"
curl -X GET "$BASE_URL/api/external/stats/" \
  -H "X-API-KEY: test-key-12345" | jq .

echo -e "\n"

# 13. 外部APIレシピ一覧
echo "13. 外部APIレシピ一覧"
curl -X GET "$BASE_URL/api/external/recipes/" \
  -H "X-API-KEY: test-key-12345" | jq .

echo -e "\n"

echo "=== テスト完了 ==="