# Daily Dish SQL Server 対応オプション

## オプション比較

| サービス | 月額コスト | SQL Server対応 | 設定難易度 | 学習価値 |
|---------|------------|---------------|------------|----------|
| **Railway + 外部SQL** | $5〜25 | 完全対応 | 高 | ⭐⭐⭐⭐ |
| **Azure App Service** | $10〜30 | Native対応 | 中 | ⭐⭐⭐⭐⭐ |
| **AWS Beanstalk** | $15〜40 | RDS対応 | 高 | ⭐⭐⭐⭐ |
| **Railway + PostgreSQL** | $0〜10 | 代替DB | 低 | ⭐⭐⭐ |

## オプション1: Railway + Azure SQL Database

### 構成
```
Railway (Django App) → Azure SQL Database
```

### 設定手順
1. **Azure SQL Database 作成**
   - Basic tier: $5/月〜
   - 接続文字列取得

2. **Railway環境変数設定**
   ```
   SQL_DB_HOST=your-server.database.windows.net
   SQL_DB_NAME=daily_dish
   SQL_DB_USER=your-username
   SQL_DB_PASSWORD=your-password
   SQL_DB_PORT=1433
   ```

3. **Dependencies変更**
   ```
   pip install mssql-django pyodbc
   ```

### メリット・デメリット
✅ 本格的なSQL Server機能  
✅ Azureクラウド学習  
❌ 設定が複雑  
❌ コストが高め

## オプション2: Azure App Service + Azure SQL

### 構成
```
Azure App Service (Django) → Azure SQL Database
```

### 月額コスト
- **App Service Basic**: $13/月
- **SQL Database Basic**: $5/月
- **合計**: 約$18/月

### 設定手順
1. **Azure リソース作成**
   ```bash
   az group create --name daily-dish-rg --location japaneast
   az sql server create --name daily-dish-server --resource-group daily-dish-rg
   az sql db create --name daily-dish-db --server daily-dish-server
   az appservice plan create --name daily-dish-plan --resource-group daily-dish-rg
   az webapp create --name daily-dish-app --plan daily-dish-plan
   ```

2. **デプロイ設定**
   ```bash
   az webapp deployment source config --name daily-dish-app --repo-url <GITHUB_URL>
   ```

### メリット・デメリット
✅ Native SQL Server対応  
✅ Microsoft環境統合  
✅ 企業での採用率高  
❌ コストが高い  
❌ Azure学習が必要

## オプション3: AWS Elastic Beanstalk + RDS SQL Server

### 構成
```
Elastic Beanstalk (Django) → RDS SQL Server
```

### 月額コスト
- **EB t3.micro**: $8/月
- **RDS SQL Server micro**: $13/月
- **合計**: 約$21/月

### 設定手順
1. **EB Application作成**
2. **RDS SQL Server インスタンス作成**
3. **環境変数設定**
4. **デプロイ**

### メリット・デメリット
✅ AWS生態系  
✅ エンタープライズ級  
✅ スケーラビリティ  
❌ 高コスト  
❌ 複雑な設定

## 推奨判断基準

### SQL Server必須の場合
**推奨**: **Azure App Service + Azure SQL**
- Microsoft環境での統合性
- 企業での採用率
- 学習価値が高い

### コスト重視の場合
**推奨**: **Railway + PostgreSQL（現在の設定）**
- 無料枠活用
- 即座にデプロイ可能
- SQL Serverとの差は最小限

### 学習目的の場合
**推奨**: **Railway + Azure SQL Database**
- クラウド間連携の学習
- 比較的低コスト
- 実践的スキル

## 移行手順（Azure SQL使用時）

### 1. requirements.txt更新
```
mssql-django==1.4
pyodbc==4.0.39
```

### 2. settings.py変更
`settings_sqlserver.py`を使用

### 3. Azure SQL Database作成
```bash
# Azure CLI使用
az sql server create --name daily-dish-server
az sql db create --name daily-dish-db --server daily-dish-server
```

### 4. Railway環境変数設定
```
DJANGO_SETTINGS_MODULE=daily_dish_project.settings_sqlserver
SQL_DB_HOST=your-server.database.windows.net
SQL_DB_NAME=daily_dish
SQL_DB_USER=admin
SQL_DB_PASSWORD=your-password
```

### 5. マイグレーション実行
```bash
python manage.py migrate
```

## トラブルシューティング

### ODBC Driver エラー
**Railway環境でのODBCドライバー問題**
```dockerfile
# Dockerfile（必要時）
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    freetds-dev
```

### 接続タイムアウト
**Firewall設定確認**
- Azure SQL: IP制限解除
- 接続文字列確認

### 文字コード問題
**日本語データ対応**
```python
'OPTIONS': {
    'driver': 'ODBC Driver 17 for SQL Server',
    'extra_params': 'TrustServerCertificate=yes;CharSet=UTF-8'
},
```