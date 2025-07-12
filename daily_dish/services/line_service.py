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