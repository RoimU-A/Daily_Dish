# LINE連携実装手順書（v3）

## 1. LINE Developers Console 設定

### 1.1 LINE Bot アカウント作成

#### 1.1.1 LINE Developers Console へアクセス
1. https://developers.line.biz/console/ にアクセス
2. LINEアカウントでログイン
3. 「Create a new provider」でプロバイダー作成

#### 1.1.2 Messaging API チャネル作成
1. 「Create a Messaging API channel」を選択
2. 基本情報入力：
   ```
   Channel name: Daily Dish Bot
   Channel description: 料理レシピ管理ボット
   Category: Food & Drink
   Subcategory: Recipe
   ```
3. チャネル作成完了

### 1.2 重要な情報取得

#### 1.2.1 必要な認証情報
```bash
# .env ファイルに追加する情報
LINE_CHANNEL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # テスト用
```

#### 1.2.2 各種設定値の取得場所
- **Channel Secret**: Basic settings > Channel secret
- **Channel Access Token**: Messaging API > Channel access token (長期)
- **User ID**: アカウント情報 > Your user ID（テスト用）

### 1.3 Webhook設定

#### 1.3.1 Webhook URL設定
1. Messaging API タブを開く
2. Webhook settings で以下を設定：
   ```
   Webhook URL: https://your-domain.com/api/external/line/webhook/
   Use webhook: Enable
   ```
3. 「Verify」ボタンでテスト実行

#### 1.3.2 応答設定
1. Messaging API > LINE Official Account features
2. 以下を設定：
   ```
   Auto-reply messages: Disable
   Greeting messages: Disable  
   Webhook: Enable
   ```

## 2. Django実装詳細

### 2.1 完全なWebhook実装

```python
# daily_dish/views_line.py（完全版）
import json
import hmac
import hashlib
import base64
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User, Recipe
from .services.line_parser import LineTextParser
from .services.line_service import LineService
from .authentication import ApiKeyAuthentication
from .permissions import IsApiKeyAuthenticated

logger = logging.getLogger(__name__)

class LineWebhookMixin:
    """LINE Webhook共通処理"""
    
    @staticmethod
    def verify_signature(body, signature):
        """LINE署名検証"""
        try:
            channel_secret = settings.LINE_CHANNEL_SECRET.encode('utf-8')
            body_bytes = body.encode('utf-8')
            
            hash_digest = hmac.new(
                channel_secret,
                body_bytes,
                hashlib.sha256
            ).digest()
            
            expected_signature = base64.b64encode(hash_digest).decode('utf-8')
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Signature verification error: {str(e)}")
            return False

@csrf_exempt
@require_http_methods(["POST"])
def line_webhook(request):
    """LINE Bot Webhook メインエンドポイント"""
    try:
        # 署名検証
        signature = request.headers.get('X-Line-Signature', '')
        body = request.body.decode('utf-8')
        
        if not LineWebhookMixin.verify_signature(body, signature):
            logger.warning("Invalid LINE signature")
            return HttpResponseForbidden("Invalid signature")
        
        # JSONデータ解析
        try:
            webhook_data = json.loads(body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook data")
            return HttpResponse("Invalid JSON", status=400)
        
        # イベント処理
        events = webhook_data.get('events', [])
        line_service = LineService()
        
        for event in events:
            try:
                if event['type'] == 'message' and event['message']['type'] == 'text':
                    line_service.handle_text_message(event)
                elif event['type'] == 'follow':
                    line_service.handle_follow_event(event)
                elif event['type'] == 'unfollow':
                    line_service.handle_unfollow_event(event)
                    
            except Exception as e:
                logger.error(f"Event processing error: {str(e)}")
                continue
        
        return HttpResponse("OK", status=200)
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return HttpResponse("Internal Server Error", status=500)

# 既存のAPI（変更なし）
@api_view(['POST'])
@permission_classes([IsApiKeyAuthenticated])
def link_line_user(request):
    """LINEユーザー紐づけAPI"""
    # 既存のコードそのまま
    pass

@api_view(['POST'])
@permission_classes([IsApiKeyAuthenticated])  
def register_recipe_from_line(request):
    """LINEレシピ登録API"""
    # 既存のコードそのまま
    pass
```

### 2.2 LINE Service実装

```python
# daily_dish/services/line_service.py
import json
import requests
import logging
from django.conf import settings
from django.core.cache import cache
from .line_parser import LineTextParser
from ..models import User, Recipe

logger = logging.getLogger(__name__)

class LineService:
    """LINE Bot サービス"""
    
    def __init__(self):
        self.access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
        self.api_url = "https://api.line.me/v2/bot"
        self.parser = LineTextParser()
    
    def send_message(self, user_id: str, message: str):
        """LINEメッセージ送信"""
        url = f"{self.api_url}/message/push"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        data = {
            'to': user_id,
            'messages': [
                {
                    'type': 'text',
                    'text': message
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            logger.info(f"Message sent to {user_id}: {message[:50]}...")
        except requests.RequestException as e:
            logger.error(f"Failed to send message: {str(e)}")
    
    def handle_text_message(self, event):
        """テキストメッセージ処理"""
        line_user_id = event['source']['userId']
        message_text = event['message']['text']
        
        # セッション状態確認
        if self.is_waiting_for_user_id(line_user_id):
            self.handle_user_id_input(line_user_id, message_text)
            return
        
        # テキスト分類
        text_type = self.parser.classify_text_type(message_text)
        
        if text_type == "user_linking":
            self.handle_user_linking_request(line_user_id)
        elif text_type == "recipe":
            self.handle_recipe_registration(line_user_id, message_text)
        elif text_type == "url":
            self.handle_url_recipe_registration(line_user_id, message_text)
        else:
            self.send_help_message(line_user_id)
    
    def handle_user_linking_request(self, line_user_id: str):
        """ユーザー紐づけリクエスト処理"""
        # セッション状態設定（5分間有効）
        cache.set(f"linking:{line_user_id}", "waiting", 300)
        
        message = """ユーザー紐づけを開始します。
        
Daily Dishアプリでアカウントを作成済みの場合は、ユーザーIDを送信してください。

まだアカウントをお持ちでない場合は、以下のURLからアプリにアクセスしてアカウントを作成してください：
https://your-app-domain.com/register"""
        
        self.send_message(line_user_id, message)
    
    def handle_user_id_input(self, line_user_id: str, user_id_str: str):
        """ユーザーID入力処理"""
        try:
            # ユーザーID妥当性チェック
            user_id = int(user_id_str.strip())
            user = User.objects.get(id=user_id)
            
            # 既存連携チェック
            if user.line_user_id:
                self.send_message(line_user_id, "このユーザーは既に他のLINEアカウントと連携済みです。")
                self.clear_user_linking_state(line_user_id)
                return
            
            # LINE重複チェック
            if User.objects.filter(line_user_id=line_user_id).exists():
                self.send_message(line_user_id, "このLINEアカウントは他のユーザーと連携済みです。")
                self.clear_user_linking_state(line_user_id)
                return
            
            # 紐づけ実行
            user.line_user_id = line_user_id
            user.save()
            
            self.send_message(
                line_user_id, 
                f"ユーザー「{user.username}」との紐づけが完了しました！\n\nこれでレシピの登録ができるようになりました。"
            )
            self.clear_user_linking_state(line_user_id)
            
        except (ValueError, User.DoesNotExist):
            self.send_message(line_user_id, "指定されたユーザーIDが見つかりません。正しいIDを入力してください。")
        except Exception as e:
            logger.error(f"User linking error: {str(e)}")
            self.send_message(line_user_id, "エラーが発生しました。しばらく時間をおいて再度お試しください。")
            self.clear_user_linking_state(line_user_id)
    
    def handle_recipe_registration(self, line_user_id: str, message_text: str):
        """レシピ登録処理"""
        try:
            # ユーザー存在確認
            user = User.objects.get(line_user_id=line_user_id)
            
            # テキスト解析
            parsed_data = self.parser.parse_recipe_text(message_text)
            recipe_data = self.parser.create_recipe_data(
                parsed_data['recipe_name'],
                parsed_data['ingredients'],
                parsed_data['amounts']
            )
            
            # レシピ作成
            ingredients_data = recipe_data.pop('ingredients_data')
            recipe_data['user'] = user
            
            recipe = Recipe.objects.create(**recipe_data)
            
            # 成功メッセージ
            ingredients_text = "\n".join([
                f"・{ing['name']} {ing['amount']}{ing['unit']}" 
                for ing in ingredients_data
            ])
            
            message = f"""レシピ「{recipe.recipe_name}」が登録されました！

【材料】
{ingredients_text}

Daily Dishアプリで詳細を確認できます。"""
            
            self.send_message(line_user_id, message)
            
        except User.DoesNotExist:
            self.send_message(
                line_user_id, 
                "ユーザー登録が完了していません。\n\n「ユーザー紐づけ」と送信してアカウント連携を行ってください。"
            )
        except Exception as e:
            logger.error(f"Recipe registration error: {str(e)}")
            self.send_message(line_user_id, f"レシピ登録でエラーが発生しました：{str(e)}")
    
    def handle_url_recipe_registration(self, line_user_id: str, url: str):
        """URL レシピ登録処理（将来実装）"""
        self.send_message(line_user_id, "URL解析機能は現在開発中です。しばらくお待ちください。")
    
    def handle_follow_event(self, event):
        """フォローイベント処理"""
        line_user_id = event['source']['userId']
        
        welcome_message = """Daily Dish Botへようこそ！

このボットでは以下のことができます：
📝 レシピの登録
🔗 アカウント連携

まずはアカウント連携から始めましょう。
「ユーザー紐づけ」と送信してください。

【レシピ登録の形式】
レシピ:料理名
材料:材料1、材料2、材料3
量:量1、量2、量3

例：
レシピ:チキンカレー
材料:鶏肉、玉ねぎ、カレールー
量:300g、200g、1箱"""
        
        self.send_message(line_user_id, welcome_message)
    
    def handle_unfollow_event(self, event):
        """アンフォローイベント処理"""
        line_user_id = event['source']['userId']
        
        # LINE連携解除（オプション）
        try:
            user = User.objects.get(line_user_id=line_user_id)
            user.line_user_id = None
            user.save()
            logger.info(f"LINE unlinking for user: {user.username}")
        except User.DoesNotExist:
            pass
    
    def send_help_message(self, line_user_id: str):
        """ヘルプメッセージ送信"""
        help_message = """認識できない形式です。

【利用可能な機能】
🔗 ユーザー紐づけ
📝 レシピ登録

【レシピ登録の形式】
レシピ:料理名
材料:材料1、材料2、材料3
量:量1、量2、量3

例：
レシピ:チキンカレー
材料:鶏肉、玉ねぎ、カレールー
量:300g、200g、1箱

アカウント連携がお済みでない場合は「ユーザー紐づけ」と送信してください。"""
        
        self.send_message(line_user_id, help_message)
    
    # セッション管理メソッド
    def is_waiting_for_user_id(self, line_user_id: str) -> bool:
        """ユーザーID入力待機中かチェック"""
        return cache.get(f"linking:{line_user_id}") == "waiting"
    
    def clear_user_linking_state(self, line_user_id: str):
        """ユーザー紐づけ状態をクリア"""
        cache.delete(f"linking:{line_user_id}")
```

### 2.3 設定ファイル完全版

```python
# daily_dish_project/settings.py への追加
import os

# LINE Bot API設定
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', '')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')

# Webhook URL検証用
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'your-domain.com',  # 本番ドメイン
    'your-ngrok-url.ngrok.io',  # 開発時のngrok URL
]

# CSRF除外（Webhook用）
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.com',
    'https://your-ngrok-url.ngrok.io',
]

# セッション管理（Redis）
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 300,  # 5分間
    }
}

# ログ設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'line_bot.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'daily_dish.services.line_service': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'daily_dish.views_line': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## 3. デプロイメント設定

### 3.1 環境変数設定

```bash
# .env ファイル完全版
# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost

# データベース
DATABASE_URL=your-database-url

# LINE Bot API
LINE_CHANNEL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Redis
REDIS_URL=redis://localhost:6379/1

# 外部API（将来実装）
RECIPE_PARSER_API_URL=https://your-recipe-parser-api.com/api/parse
RECIPE_PARSER_API_KEY=your-recipe-parser-api-key-here
```

### 3.2 Railway デプロイ設定

```bash
# railway.json への追加
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  },
  "environments": {
    "production": {
      "variables": {
        "LINE_CHANNEL_SECRET": "${{LINE_CHANNEL_SECRET}}",
        "LINE_CHANNEL_ACCESS_TOKEN": "${{LINE_CHANNEL_ACCESS_TOKEN}}",
        "REDIS_URL": "${{REDIS_URL}}"
      }
    }
  }
}
```

### 3.3 ngrok 開発環境設定

```bash
# 開発時のngrok設定
ngrok config add-authtoken your-ngrok-authtoken

# Webhook URL用のトンネル作成
ngrok http 8000 --domain=your-static-domain.ngrok.io

# LINE Webhook URL設定
# https://your-static-domain.ngrok.io/api/external/line/webhook/
```

## 4. テスト手順

### 4.1 Webhook接続テスト

```python
# テスト用のcURLコマンド
curl -X POST https://your-domain.com/api/external/line/webhook/ \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test-signature" \
  -d '{
    "events": [
      {
        "type": "message",
        "message": {
          "type": "text",
          "text": "テストメッセージ"
        },
        "source": {
          "userId": "U1234567890abcdef1234567890abcdef"
        }
      }
    ]
  }'
```

### 4.2 LINE Bot実動テスト手順

1. **友達追加テスト**
   - LINE Developers Console > Messaging API > QR code
   - QRコードを読み取って友達追加
   - ウェルカムメッセージ確認

2. **ユーザー紐づけテスト**
   - 「ユーザー紐づけ」メッセージ送信
   - ユーザーID入力（事前にWebアプリでアカウント作成）
   - 成功メッセージ確認

3. **レシピ登録テスト**
   ```
   レシピ:テストカレー
   材料:鶏肉、玉ねぎ、人参
   量:300g、200g、150g
   ```
   - 上記メッセージ送信
   - 成功メッセージ確認
   - Webアプリでレシピ登録確認

### 4.3 監視・ログ確認

```bash
# ログ確認
tail -f line_bot.log

# Redis セッション確認
redis-cli
> KEYS linking:*
> GET "linking:U1234567890abcdef1234567890abcdef"
```

## 5. トラブルシューティング

### 5.1 よくある問題

#### 5.1.1 Webhook が呼ばれない
- LINE Developers Console の Webhook URL 設定確認
- HTTPS 必須（ngrokでテスト可能）
- レスポンス200必須

#### 5.1.2 署名検証エラー
- `LINE_CHANNEL_SECRET` 設定確認
- リクエストボディの文字コード確認

#### 5.1.3 メッセージ送信失敗
- `LINE_CHANNEL_ACCESS_TOKEN` 設定確認
- アクセストークンの有効期限確認

### 5.2 デバッグ設定

```python
# settings.py でデバッグモード
LOGGING['loggers']['daily_dish.services.line_service']['level'] = 'DEBUG'

# views_line.py でデバッグログ追加
logger.debug(f"Received webhook data: {webhook_data}")
logger.debug(f"Processing event: {event}")
```

---

この実装手順書により、LINE連携機能の完全な実装が可能になります。特にWebhookの設定と署名検証が重要なポイントです。