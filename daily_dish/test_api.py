from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime

from .models import Recipe, RegisteredRecipe, CookedDish, IngredientCache, ApiKey

User = get_user_model()


class WebAPIAuthenticationTest(APITestCase):
    """Web API認証テスト"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_user_registration(self):
        """ユーザー登録テスト"""
        url = reverse('daily_dish:web_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_jwt_login(self):
        """JWT認証ログインテスト"""
        url = reverse('daily_dish:web_login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_jwt_protected_endpoint(self):
        """JWT認証が必要なエンドポイントのテスト"""
        # ログインしてトークン取得
        login_url = reverse('daily_dish:web_login')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        login_response = self.client.post(login_url, login_data)
        access_token = login_response.data['access']
        
        # 認証ヘッダーを設定してAPIアクセス
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('daily_dish:web_profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class ExternalAPIAuthenticationTest(APITestCase):
    """外部API認証テスト"""
    
    def setUp(self):
        self.api_key = ApiKey.objects.create(
            key_name='テスト用API Key',
            api_key='test-api-key-12345'
        )
    
    def test_api_key_authentication(self):
        """API Key認証テスト"""
        self.client.credentials(HTTP_X_API_KEY='test-api-key-12345')
        
        url = reverse('daily_dish:external_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_recipes', response.data)
    
    def test_invalid_api_key(self):
        """無効なAPI Keyテスト"""
        self.client.credentials(HTTP_X_API_KEY='invalid-key')
        
        url = reverse('daily_dish:external_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_api_key(self):
        """API Key未設定テスト"""
        url = reverse('daily_dish:external_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeAPITest(APITestCase):
    """レシピAPIテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )
        
        # JWT認証でログイン
        login_url = reverse('daily_dish:web_login')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        login_response = self.client.post(login_url, login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.recipe_data = {
            'recipe_name': 'テストレシピ',
            'ingredient_1': '鶏肉',
            'amount_1': '300.0',
            'unit_1': 'g',
            'ingredient_2': '玉ねぎ',
            'amount_2': '200.0',
            'unit_2': 'g'
        }
    
    def test_recipe_creation(self):
        """レシピ作成テスト"""
        url = reverse('daily_dish:web_recipe_list')
        response = self.client.post(url, self.recipe_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recipe_name'], 'テストレシピ')
        self.assertEqual(len(response.data['ingredients']), 2)
    
    def test_recipe_list(self):
        """レシピ一覧取得テスト"""
        Recipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ1',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
        Recipe.objects.create(
            user=self.user2,  # 他のユーザーのレシピ
            recipe_name='テストレシピ2',
            ingredient_1='材料B',
            amount_1=Decimal('200.0'),
            unit_1='g'
        )
        
        url = reverse('daily_dish:web_recipe_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 自分のレシピのみ取得されることを確認
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['recipe_name'], 'テストレシピ1')
    
    def test_recipe_update(self):
        """レシピ更新テスト"""
        recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
        
        url = reverse('daily_dish:web_recipe_detail', kwargs={'pk': recipe.pk})
        update_data = {
            'recipe_name': '更新されたレシピ',
            'ingredient_1': '更新された材料A',
            'amount_1': '150.0',
            'unit_1': 'g'
        }
        response = self.client.patch(url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe_name'], '更新されたレシピ')
    
    def test_recipe_delete(self):
        """レシピ削除テスト"""
        recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
        
        url = reverse('daily_dish:web_recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe.pk).exists())


class RegisteredRecipeAPITest(APITestCase):
    """登録済みレシピAPIテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # JWT認証でログイン
        login_url = reverse('daily_dish:web_login')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        login_response = self.client.post(login_url, login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='新規レシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
    
    def test_existing_recipe_registration(self):
        """既存レシピ登録テスト"""
        url = reverse('daily_dish:web_registered_recipe_list')
        data = {
            'recipe_name': '既存レシピ',
            'recipe_type': 'existing',
            'recipe_url': 'https://example.com/recipe/123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recipe_type'], 'existing')
        self.assertEqual(response.data['recipe_url'], 'https://example.com/recipe/123')
    
    def test_new_recipe_registration(self):
        """新規レシピ登録テスト"""
        url = reverse('daily_dish:web_registered_recipe_list')
        data = {
            'recipe_name': '新規レシピ',
            'recipe_type': 'new',
            'recipe': self.recipe.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recipe_type'], 'new')
        self.assertEqual(response.data['recipe'], self.recipe.pk)


class ExternalAPITest(APITestCase):
    """外部APIテスト"""
    
    def setUp(self):
        self.api_key = ApiKey.objects.create(
            key_name='テスト用API Key',
            api_key='test-api-key-12345'
        )
        self.client.credentials(HTTP_X_API_KEY='test-api-key-12345')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
    
    def test_external_recipe_list(self):
        """外部API レシピ一覧テスト"""
        url = reverse('daily_dish:external_recipe_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['recipe_name'], 'テストレシピ')
    
    def test_external_stats(self):
        """外部API 統計情報テスト"""
        url = reverse('daily_dish:external_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_recipes', response.data)
        self.assertIn('total_users', response.data)
        self.assertEqual(response.data['total_recipes'], 1)
        self.assertEqual(response.data['total_users'], 1)


class PermissionTest(APITestCase):
    """権限テスト"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpassword123'
        )
        
        self.recipe = Recipe.objects.create(
            user=self.user1,
            recipe_name='User1のレシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
    
    def test_other_user_recipe_access_denied(self):
        """他のユーザーのレシピアクセス拒否テスト"""
        # user2でログイン
        login_url = reverse('daily_dish:web_login')
        login_data = {
            'username': 'user2',
            'password': 'testpassword123'
        }
        login_response = self.client.post(login_url, login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # user1のレシピにアクセスを試行
        url = reverse('daily_dish:web_recipe_detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)