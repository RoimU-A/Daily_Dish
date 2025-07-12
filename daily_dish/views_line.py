# daily_dish/views_line.py
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

@api_view(['POST'])
@permission_classes([IsApiKeyAuthenticated])
def link_line_user(request):
    """LINEユーザー紐づけAPI"""
    try:
        line_user_id = request.data.get('line_user_id')
        app_user_id = request.data.get('app_user_id')
        
        # バリデーション
        if not line_user_id or not app_user_id:
            return Response({
                'status': 'error',
                'error_code': 'MISSING_PARAMETERS',
                'message': 'line_user_idとapp_user_idが必要です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ユーザー存在確認
        try:
            user = User.objects.get(id=app_user_id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'error_code': 'USER_NOT_FOUND',
                'message': '指定されたユーザーIDが見つかりません'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 既存連携チェック
        if user.line_user_id:
            return Response({
                'status': 'error',
                'error_code': 'ALREADY_LINKED',
                'message': 'このユーザーは既に他のLINEアカウントと連携済みです'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # LINE重複チェック
        if User.objects.filter(line_user_id=line_user_id).exists():
            return Response({
                'status': 'error',
                'error_code': 'LINE_ALREADY_USED',
                'message': 'このLINEアカウントは他のユーザーと連携済みです'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 紐づけ実行
        user.line_user_id = line_user_id
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'ユーザー紐づけが完了しました',
            'user': {
                'id': user.id,
                'username': user.username,
                'line_user_id': user.line_user_id
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"LINE user linking error: {str(e)}")
        return Response({
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': '内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsApiKeyAuthenticated])
def register_recipe_from_line(request):
    """LINEレシピ登録API"""
    try:
        line_user_id = request.data.get('line_user_id')
        text = request.data.get('text')
        
        # バリデーション
        if not line_user_id or not text:
            return Response({
                'status': 'error',
                'error_code': 'MISSING_PARAMETERS',
                'message': 'line_user_idとtextが必要です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ユーザー取得
        try:
            user = User.objects.get(line_user_id=line_user_id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'error_code': 'USER_NOT_LINKED',
                'message': 'ユーザー登録が完了していません。まず当アプリでアカウントを作成し、ユーザー紐づけを行ってください。'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # テキスト解析
        parser = LineTextParser()
        text_type = parser.classify_text_type(text)
        
        if text_type == "user_linking":
            return Response({
                'status': 'info',
                'message': 'ユーザー紐づけは別のAPIを使用してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif text_type == "recipe":
            # 新規レシピ登録
            try:
                parsed_data = parser.parse_recipe_text(text)
                recipe_data = parser.create_recipe_data(
                    parsed_data['recipe_name'],
                    parsed_data['ingredients'],
                    parsed_data['amounts']
                )
                
                # レシピ作成
                ingredients_data = recipe_data.pop('ingredients_data')
                recipe_data['user'] = user
                
                recipe = Recipe.objects.create(**recipe_data)
                
                return Response({
                    'status': 'success',
                    'message': 'レシピが登録されました',
                    'recipe': {
                        'id': recipe.id,
                        'recipe_name': recipe.recipe_name,
                        'recipe_url': recipe.recipe_url,
                        'ingredients': ingredients_data,
                        'created_at': recipe.created_at.isoformat()
                    }
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'status': 'error',
                    'error_code': 'PARSE_ERROR',
                    'message': f'テキストの解析に失敗しました: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        elif text_type == "url":
            # 既存レシピ登録（将来実装）
            return Response({
                'status': 'error',
                'error_code': 'NOT_IMPLEMENTED',
                'message': 'URL解析機能は現在開発中です'
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
        
        else:
            # 不明な形式
            return Response({
                'status': 'error',
                'error_code': 'INVALID_FORMAT',
                'message': '認識できない形式です。\n\n利用可能な形式:\n- ユーザー紐づけ\n- レシピ:○○\n材料:材料1、材料2\n量:量1、量2'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"LINE recipe registration error: {str(e)}")
        return Response({
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': '内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)