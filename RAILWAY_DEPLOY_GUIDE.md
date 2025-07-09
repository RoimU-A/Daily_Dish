# Daily Dish Railway デプロイガイド

## 事前準備

### 1. Railwayアカウント作成
1. https://railway.app にアクセス
2. GitHubアカウントでログイン
3. 無料$5クレジットを確認

### 2. 必要なファイル確認
以下のファイルが準備済みであることを確認：
- `requirements.txt` - 更新済み
- `railway.json` - 新規作成済み
- `nixpacks.toml` - 新規作成済み
- `settings.py` - Railway対応済み

## デプロイ手順

### ステップ1: GitHubリポジトリ準備
```bash
# Gitリポジトリの初期化（まだの場合）
git init
git add .
git commit -m "Initial commit for Railway deployment"

# GitHubリポジトリ作成後
git remote add origin https://github.com/YOUR_USERNAME/daily-dish.git
git branch -M main
git push -u origin main
```

### ステップ2: Railway プロジェクト作成
1. Railway ダッシュボードにログイン
2. "New Project" をクリック
3. "Deploy from GitHub repo" を選択
4. `daily-dish` リポジトリを選択

### ステップ3: PostgreSQL データベース追加
1. プロジェクト画面で "Add Service" をクリック
2. "Database" → "PostgreSQL" を選択
3. 自動でデータベースが作成される

### ステップ4: 環境変数設定
Railway プロジェクトの Variables タブで以下を設定：

```
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
DATABASE_URL=（自動設定されます）
RAILWAY_ENVIRONMENT_NAME=production
```

**SECRET_KEY生成方法**:
```python
# Pythonで実行
import secrets
print(secrets.token_urlsafe(50))
```

### ステップ5: 初回デプロイ
1. Railway が自動的にビルド・デプロイを開始
2. Logs タブでデプロイ状況を確認
3. ビルド完了後、URLを確認

### ステップ6: データベース初期化
Railway Console で以下を実行：
```bash
python manage.py migrate
python manage.py createsuperuser
```

## デプロイ後の設定

### 1. API Key 作成
Django Admin または create_api_key.py スクリプトで API Key を作成

### 2. 動作確認
- `/admin/` - Django Admin アクセス
- `/api/web/` - API エンドポイント確認
- `/api/external/stats/` - 外部API確認（API Key必要）

## 予想される問題と解決策

### 問題1: ビルドエラー
**症状**: requirements.txt でエラー
**解決**: 依存関係の競合確認、バージョン固定

### 問題2: データベース接続エラー
**症状**: DATABASE_URL not found
**解決**: PostgreSQL サービスが追加されているか確認

### 問題3: 静的ファイルエラー
**症状**: CSS/JS が読み込まれない
**解決**: `python manage.py collectstatic` 実行確認

### 問題4: CORS エラー
**症状**: フロントエンドからのアクセスが拒否
**解決**: CORS_ALLOWED_ORIGINS の設定確認

## 運用

### 更新デプロイ
```bash
git add .
git commit -m "Update: 変更内容"
git push origin main
```
→ Railway が自動的に再デプロイ

### ログ確認
Railway ダッシュボードの Logs タブで確認

### データベースバックアップ
定期的にデータエクスポートを実行推奨

## コスト管理

### 料金体系
- 使用量ベース課金
- 月額$5クレジット無料
- 超過分は従量課金

### コスト削減
1. 不要なサービス削除
2. スリープ機能活用
3. 使用量監視

## トラブルシューティング

### デバッグモード一時有効化
環境変数で `DEBUG=True` に設定（本番では即座に戻す）

### データベースリセット
```bash
python manage.py flush
python manage.py migrate
```

### ログレベル変更
環境変数で `LOG_LEVEL=DEBUG` に設定