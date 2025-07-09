# Daily Dish サンプルデータテスト仕様書

## テスト概要
- **目的**: ユーザー登録、既存レシピ登録、新規レシピ登録の機能をサンプルデータで検証
- **前提**: 外部アプリは未実装のため、正常なデータが送られてきたと想定
- **データベース**: SQLite（開発環境）

## テストケース一覧

### TC001: ユーザー登録テスト
**テスト内容**: 新規ユーザーの登録
**入力データ**:
```json
{
  "username": "yamada_taro",
  "email": "yamada@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**想定結果（DB）**:
- usersテーブルに新規レコード追加
- id: 自動採番
- username: "yamada_taro"
- email: "yamada@example.com"
- is_active: true
- created_at: 実行時刻
- updated_at: 実行時刻

### TC002: 新規レシピ登録テスト
**テスト内容**: ユーザーが独自レシピを登録
**前提**: TC001のユーザーでログイン済み
**入力データ**:
```json
{
  "recipe_name": "山田家の肉じゃが",
  "ingredient_1": "じゃがいも",
  "amount_1": "4.0",
  "unit_1": "個",
  "ingredient_2": "にんじん",
  "amount_2": "1.0", 
  "unit_2": "本",
  "ingredient_3": "玉ねぎ",
  "amount_3": "1.0",
  "unit_3": "個",
  "ingredient_4": "牛肉",
  "amount_4": "300.0",
  "unit_4": "g",
  "ingredient_5": "しらたき",
  "amount_5": "1.0",
  "unit_5": "袋"
}
```

**想定結果（DB）**:
- recipesテーブルに新規レコード追加
- id: 自動採番
- user_id: TC001で作成したユーザーのID
- recipe_name: "山田家の肉じゃが"
- ingredient_1〜5: 上記データ
- ingredient_6〜20: NULL
- created_at: 実行時刻

### TC003: 既存レシピ登録テスト
**テスト内容**: 外部サイトのレシピURLを登録
**前提**: TC001のユーザーでログイン済み
**入力データ**:
```json
{
  "recipe_name": "クックパッドの鶏の唐揚げ",
  "recipe_type": "existing",
  "recipe_url": "https://cookpad.com/recipe/2858078"
}
```

**想定結果（DB）**:
- registered_recipesテーブルに新規レコード追加
- id: 自動採番
- user_id: TC001で作成したユーザーのID
- recipe_name: "クックパッドの鶏の唐揚げ"
- recipe_type: "existing"
- recipe_url: "https://cookpad.com/recipe/2858078"
- recipe_id: NULL
- created_at: 実行時刻

### TC004: 新規レシピの登録済みレシピ化テスト
**テスト内容**: TC002で作成したレシピを登録済みレシピとして登録
**前提**: TC001のユーザーでログイン済み、TC002のレシピ作成済み
**入力データ**:
```json
{
  "recipe_name": "山田家の肉じゃが",
  "recipe_type": "new",
  "recipe": [TC002で作成されたレシピID]
}
```

**想定結果（DB）**:
- registered_recipesテーブルに新規レコード追加
- id: 自動採番
- user_id: TC001で作成したユーザーのID
- recipe_name: "山田家の肉じゃが"
- recipe_type: "new"
- recipe_url: NULL
- recipe_id: TC002で作成されたレシピのID
- created_at: 実行時刻

### TC005: 食材キャッシュ登録テスト
**テスト内容**: TC002のレシピから食材をキャッシュに追加
**前提**: TC001のユーザーでログイン済み
**入力データ**:
```json
[
  {
    "ingredient_name": "じゃがいも",
    "amount": "4.0",
    "unit": "個"
  },
  {
    "ingredient_name": "にんじん", 
    "amount": "1.0",
    "unit": "本"
  },
  {
    "ingredient_name": "玉ねぎ",
    "amount": "1.0", 
    "unit": "個"
  },
  {
    "ingredient_name": "牛肉",
    "amount": "300.0",
    "unit": "g"
  },
  {
    "ingredient_name": "しらたき",
    "amount": "1.0",
    "unit": "袋"
  }
]
```

**想定結果（DB）**:
- ingredient_cacheテーブルに5件のレコード追加
- 各レコードのuser_id: TC001で作成したユーザーのID
- ingredient_name, amount, unit: 上記データ通り
- created_at: 実行時刻

## 検証ポイント
1. データの整合性
2. 外部キー制約の正常動作
3. バリデーションの正常動作
4. 日本語データの正常処理
5. Decimal型の正確な保存