from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Recipe, RegisteredRecipe, CookedDish, IngredientCache, ApiKey

User = get_user_model()


class UserModelTest(TestCase):
    """ユーザーモデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
    
    def test_user_creation(self):
        """ユーザーの作成テスト"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
    
    def test_user_str_method(self):
        """__str__メソッドのテスト"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_unique_email_constraint(self):
        """メールアドレスのユニーク制約テスト"""
        User.objects.create_user(**self.user_data)
        
        # 同じメールアドレスでの重複作成
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'testuser2'
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_data)
    
    def test_unique_username_constraint(self):
        """ユーザー名のユニーク制約テスト"""
        User.objects.create_user(**self.user_data)
        
        # 同じユーザー名での重複作成
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'test2@example.com'
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_data)


class RecipeModelTest(TestCase):
    """レシピモデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.recipe_data = {
            'user': self.user,
            'recipe_name': 'テストレシピ',
            'ingredient_1': '鶏肉',
            'amount_1': Decimal('300.0'),
            'unit_1': 'g',
            'ingredient_2': '玉ねぎ',
            'amount_2': Decimal('200.0'),
            'unit_2': 'g',
        }
    
    def test_recipe_creation(self):
        """レシピの作成テスト"""
        recipe = Recipe.objects.create(**self.recipe_data)
        
        self.assertEqual(recipe.recipe_name, 'テストレシピ')
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.ingredient_1, '鶏肉')
        self.assertEqual(recipe.amount_1, Decimal('300.0'))
        self.assertEqual(recipe.unit_1, 'g')
        self.assertIsNotNone(recipe.created_at)
        self.assertIsNotNone(recipe.updated_at)
    
    def test_recipe_str_method(self):
        """__str__メソッドのテスト"""
        recipe = Recipe.objects.create(**self.recipe_data)
        expected = f"テストレシピ by {self.user.username}"
        self.assertEqual(str(recipe), expected)
    
    def test_get_ingredients_method(self):
        """get_ingredients()メソッドのテスト"""
        recipe = Recipe.objects.create(**self.recipe_data)
        ingredients = recipe.get_ingredients()
        
        expected = [
            {'name': '鶏肉', 'amount': 300.0, 'unit': 'g'},
            {'name': '玉ねぎ', 'amount': 200.0, 'unit': 'g'}
        ]
        
        self.assertEqual(ingredients, expected)
    
    def test_get_ingredients_with_empty_fields(self):
        """空のフィールドがあるときのget_ingredients()テスト"""
        # 材料1のみ設定
        recipe_data = {
            'user': self.user,
            'recipe_name': 'シンプルレシピ',
            'ingredient_1': '塩',
            'amount_1': Decimal('5.0'),
            'unit_1': 'g',
        }
        recipe = Recipe.objects.create(**recipe_data)
        ingredients = recipe.get_ingredients()
        
        expected = [
            {'name': '塩', 'amount': 5.0, 'unit': 'g'}
        ]
        
        self.assertEqual(ingredients, expected)
    
    def test_get_ingredients_with_partial_data(self):
        """不完全なデータのときのget_ingredients()テスト"""
        # 材料名はあるが分量がない場合
        recipe_data = {
            'user': self.user,
            'recipe_name': '不完全レシピ',
            'ingredient_1': '材料A',
            'amount_1': None,  # 分量なし
            'unit_1': 'g',
        }
        recipe = Recipe.objects.create(**recipe_data)
        ingredients = recipe.get_ingredients()
        
        # 不完全なデータは除外される
        self.assertEqual(ingredients, [])
    
    def test_foreign_key_relationship(self):
        """外部キー関係のテスト"""
        recipe = Recipe.objects.create(**self.recipe_data)
        
        # ユーザーからレシピが取得できる
        user_recipes = self.user.recipe_set.all()
        self.assertIn(recipe, user_recipes)


class RegisteredRecipeModelTest(TestCase):
    """登録済みレシピモデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # 新規レシピ用
        self.recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='新規レシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
    
    def test_existing_recipe_creation(self):
        """既存レシピ登録のテスト"""
        registered = RegisteredRecipe.objects.create(
            user=self.user,
            recipe_name='既存レシピ',
            recipe_type='existing',
            recipe_url='https://example.com/recipe/123'
        )
        
        self.assertEqual(registered.recipe_type, 'existing')
        self.assertEqual(registered.recipe_url, 'https://example.com/recipe/123')
        self.assertIsNone(registered.recipe)
    
    def test_new_recipe_creation(self):
        """新規レシピ登録のテスト"""
        registered = RegisteredRecipe.objects.create(
            user=self.user,
            recipe_name='新規レシピ',
            recipe_type='new',
            recipe=self.recipe
        )
        
        self.assertEqual(registered.recipe_type, 'new')
        self.assertEqual(registered.recipe, self.recipe)
        self.assertIsNone(registered.recipe_url)
    
    def test_registered_recipe_str_method(self):
        """__str__メソッドのテスト"""
        registered = RegisteredRecipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ',
            recipe_type='existing',
            recipe_url='https://example.com/recipe/123'
        )
        
        expected = f"テストレシピ (existing) by {self.user.username}"
        self.assertEqual(str(registered), expected)
    
    def test_clean_method_existing_valid(self):
        """既存レシピのバリデーション（正常）"""
        registered = RegisteredRecipe(
            user=self.user,
            recipe_name='既存レシピ',
            recipe_type='existing',
            recipe_url='https://example.com/recipe/123'
        )
        
        # clean()メソッドが例外を発生させないことを確認
        try:
            registered.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
    
    def test_clean_method_new_valid(self):
        """新規レシピのバリデーション（正常）"""
        registered = RegisteredRecipe(
            user=self.user,
            recipe_name='新規レシピ',
            recipe_type='new',
            recipe=self.recipe
        )
        
        # clean()メソッドが例外を発生させないことを確認
        try:
            registered.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
    
    def test_clean_method_existing_invalid(self):
        """既存レシピのバリデーション（異常）"""
        # URLなしの既存レシピ
        registered = RegisteredRecipe(
            user=self.user,
            recipe_name='既存レシピ',
            recipe_type='existing',
            recipe_url='',  # URLなし
            recipe=self.recipe  # recipeあり（不適切）
        )
        
        with self.assertRaises(ValidationError):
            registered.clean()
    
    def test_clean_method_new_invalid(self):
        """新規レシピのバリデーション（異常）"""
        # recipeなしの新規レシピ
        registered = RegisteredRecipe(
            user=self.user,
            recipe_name='新規レシピ',
            recipe_type='new',
            recipe_url='https://example.com/recipe/123',  # URLあり（不適切）
            recipe=None  # recipeなし
        )
        
        with self.assertRaises(ValidationError):
            registered.clean()


class CookedDishModelTest(TestCase):
    """料理履歴モデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.registered_recipe = RegisteredRecipe.objects.create(
            user=self.user,
            recipe_name='テストレシピ',
            recipe_type='existing',
            recipe_url='https://example.com/recipe/123'
        )
    
    def test_cooked_dish_creation(self):
        """料理履歴の作成テスト"""
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        self.assertEqual(cooked.user, self.user)
        self.assertEqual(cooked.registered_recipe, self.registered_recipe)
        self.assertIsNotNone(cooked.created_at)
    
    def test_cooked_dish_str_method(self):
        """__str__メソッドのテスト"""
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        expected = f"テストレシピ cooked by {self.user.username} at {cooked.created_at}"
        self.assertEqual(str(cooked), expected)
    
    def test_foreign_key_relationships(self):
        """外部キー関係のテスト"""
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        # ユーザーから料理履歴が取得できる
        user_dishes = self.user.cookeddish_set.all()
        self.assertIn(cooked, user_dishes)
        
        # 登録レシピから料理履歴が取得できる
        recipe_dishes = self.registered_recipe.cookeddish_set.all()
        self.assertIn(cooked, recipe_dishes)


class IngredientCacheModelTest(TestCase):
    """食材キャッシュモデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_ingredient_cache_creation(self):
        """食材キャッシュの作成テスト"""
        cache = IngredientCache.objects.create(
            user=self.user,
            ingredient_name='鶏肉',
            amount=Decimal('300.0'),
            unit='g'
        )
        
        self.assertEqual(cache.user, self.user)
        self.assertEqual(cache.ingredient_name, '鶏肉')
        self.assertEqual(cache.amount, Decimal('300.0'))
        self.assertEqual(cache.unit, 'g')
        self.assertIsNotNone(cache.created_at)
    
    def test_ingredient_cache_str_method(self):
        """__str__メソッドのテスト"""
        cache = IngredientCache.objects.create(
            user=self.user,
            ingredient_name='鶏肉',
            amount=Decimal('300.0'),
            unit='g'
        )
        
        expected = f"鶏肉 300.0g for {self.user.username}"
        self.assertEqual(str(cache), expected)
    
    def test_unique_together_constraint(self):
        """ユニーク制約のテスト"""
        # 最初のレコード作成
        IngredientCache.objects.create(
            user=self.user,
            ingredient_name='鶏肉',
            amount=Decimal('300.0'),
            unit='g'
        )
        
        # 同じユーザー・同じ材料名での重複作成
        with self.assertRaises(IntegrityError):
            IngredientCache.objects.create(
                user=self.user,
                ingredient_name='鶏肉',  # 同じ材料名
                amount=Decimal('500.0'),  # 異なる分量
                unit='g'
            )
    
    def test_different_users_same_ingredient(self):
        """異なるユーザーの同じ材料名は許可されることのテスト"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )
        
        # ユーザー1の食材キャッシュ
        IngredientCache.objects.create(
            user=self.user,
            ingredient_name='鶏肉',
            amount=Decimal('300.0'),
            unit='g'
        )
        
        # ユーザー2の同じ材料名（これは許可される）
        cache2 = IngredientCache.objects.create(
            user=user2,
            ingredient_name='鶏肉',
            amount=Decimal('500.0'),
            unit='g'
        )
        
        self.assertEqual(cache2.user, user2)
        self.assertEqual(cache2.ingredient_name, '鶏肉')


class ApiKeyModelTest(TestCase):
    """API Keyモデルのテスト"""
    
    def test_api_key_creation(self):
        """API Keyの作成テスト"""
        api_key = ApiKey.objects.create(
            key_name='テスト用キー',
            api_key='test-api-key-12345'
        )
        
        self.assertEqual(api_key.key_name, 'テスト用キー')
        self.assertEqual(api_key.api_key, 'test-api-key-12345')
        self.assertTrue(api_key.is_active)
        self.assertEqual(api_key.usage_count, 0)
        self.assertIsNotNone(api_key.created_at)
        self.assertIsNone(api_key.expires_at)
        self.assertIsNone(api_key.last_used_at)
    
    def test_api_key_str_method(self):
        """__str__メソッドのテスト"""
        api_key = ApiKey.objects.create(
            key_name='テスト用キー',
            api_key='test-api-key-12345'
        )
        
        expected = "テスト用キー (Active)"
        self.assertEqual(str(api_key), expected)
        
        # 非アクティブの場合
        api_key.is_active = False
        api_key.save()
        
        expected = "テスト用キー (Inactive)"
        self.assertEqual(str(api_key), expected)
    
    def test_unique_api_key_constraint(self):
        """API Keyのユニーク制約テスト"""
        ApiKey.objects.create(
            key_name='キー1',
            api_key='test-api-key-12345'
        )
        
        # 同じAPI Keyでの重複作成
        with self.assertRaises(IntegrityError):
            ApiKey.objects.create(
                key_name='キー2',
                api_key='test-api-key-12345'  # 同じAPI Key
            )


class ModelRelationshipTest(TestCase):
    """モデル間の関係性テスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.recipe = Recipe.objects.create(
            user=self.user,
            recipe_name='新規レシピ',
            ingredient_1='材料A',
            amount_1=Decimal('100.0'),
            unit_1='g'
        )
        
        self.registered_recipe = RegisteredRecipe.objects.create(
            user=self.user,
            recipe_name='新規レシピ',
            recipe_type='new',
            recipe=self.recipe
        )
    
    def test_cascade_delete_user(self):
        """ユーザー削除時のカスケード削除テスト"""
        # 関連データを作成
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        cache = IngredientCache.objects.create(
            user=self.user,
            ingredient_name='テスト材料',
            amount=Decimal('100.0'),
            unit='g'
        )
        
        # ユーザー削除前のレコード数確認
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(RegisteredRecipe.objects.count(), 1)
        self.assertEqual(CookedDish.objects.count(), 1)
        self.assertEqual(IngredientCache.objects.count(), 1)
        
        # ユーザー削除
        self.user.delete()
        
        # 関連レコードがすべて削除されていることを確認
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(RegisteredRecipe.objects.count(), 0)
        self.assertEqual(CookedDish.objects.count(), 0)
        self.assertEqual(IngredientCache.objects.count(), 0)
    
    def test_cascade_delete_recipe(self):
        """レシピ削除時のカスケード削除テスト"""
        # 料理履歴を作成
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        # レシピ削除前のレコード数確認
        self.assertEqual(RegisteredRecipe.objects.count(), 1)
        self.assertEqual(CookedDish.objects.count(), 1)
        
        # レシピ削除
        self.recipe.delete()
        
        # 登録レシピと料理履歴も削除されていることを確認
        self.assertEqual(RegisteredRecipe.objects.count(), 0)
        self.assertEqual(CookedDish.objects.count(), 0)
    
    def test_cascade_delete_registered_recipe(self):
        """登録レシピ削除時のカスケード削除テスト"""
        # 料理履歴を作成
        cooked = CookedDish.objects.create(
            user=self.user,
            registered_recipe=self.registered_recipe
        )
        
        # 削除前のレコード数確認
        self.assertEqual(CookedDish.objects.count(), 1)
        
        # 登録レシピ削除
        self.registered_recipe.delete()
        
        # 料理履歴も削除されていることを確認
        self.assertEqual(CookedDish.objects.count(), 0)
        
        # 元のレシピは残っていることを確認
        self.assertEqual(Recipe.objects.count(), 1)