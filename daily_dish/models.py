from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from decimal import Decimal


class User(AbstractUser):
    """ユーザーモデル（LINE連携対応）"""
    email = models.EmailField(unique=True)
    line_user_id = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="LINEユーザーID（連携時に設定）"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['line_user_id']),
        ]
    
    @property
    def is_line_linked(self):
        """LINE連携状態の確認"""
        return bool(self.line_user_id)


class Recipe(models.Model):
    """統一レシピモデル（既存・新規両方対応）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=255)
    recipe_url = models.URLField(max_length=500, null=True, blank=True)  # URLフィールド追加
    
    # 材料1-20のフィールド
    ingredient_1 = models.CharField(max_length=100, null=True, blank=True)
    amount_1 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_1 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_2 = models.CharField(max_length=100, null=True, blank=True)
    amount_2 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_2 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_3 = models.CharField(max_length=100, null=True, blank=True)
    amount_3 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_3 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_4 = models.CharField(max_length=100, null=True, blank=True)
    amount_4 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_4 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_5 = models.CharField(max_length=100, null=True, blank=True)
    amount_5 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_5 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_6 = models.CharField(max_length=100, null=True, blank=True)
    amount_6 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_6 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_7 = models.CharField(max_length=100, null=True, blank=True)
    amount_7 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_7 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_8 = models.CharField(max_length=100, null=True, blank=True)
    amount_8 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_8 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_9 = models.CharField(max_length=100, null=True, blank=True)
    amount_9 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_9 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_10 = models.CharField(max_length=100, null=True, blank=True)
    amount_10 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_10 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_11 = models.CharField(max_length=100, null=True, blank=True)
    amount_11 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_11 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_12 = models.CharField(max_length=100, null=True, blank=True)
    amount_12 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_12 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_13 = models.CharField(max_length=100, null=True, blank=True)
    amount_13 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_13 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_14 = models.CharField(max_length=100, null=True, blank=True)
    amount_14 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_14 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_15 = models.CharField(max_length=100, null=True, blank=True)
    amount_15 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_15 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_16 = models.CharField(max_length=100, null=True, blank=True)
    amount_16 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_16 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_17 = models.CharField(max_length=100, null=True, blank=True)
    amount_17 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_17 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_18 = models.CharField(max_length=100, null=True, blank=True)
    amount_18 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_18 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_19 = models.CharField(max_length=100, null=True, blank=True)
    amount_19 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_19 = models.CharField(max_length=20, null=True, blank=True)
    
    ingredient_20 = models.CharField(max_length=100, null=True, blank=True)
    amount_20 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    unit_20 = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recipes'
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def get_ingredients(self):
        """材料リストを取得"""
        ingredients = []
        for i in range(1, 21):
            name = getattr(self, f'ingredient_{i}')
            amount = getattr(self, f'amount_{i}')
            unit = getattr(self, f'unit_{i}')
            
            if name and amount and unit:
                ingredients.append({
                    'name': name,
                    'amount': float(amount),
                    'unit': unit
                })
        return ingredients
    
    def set_ingredients(self, ingredients_data):
        """材料情報の設定（LINE入力対応）"""
        # 既存の材料フィールドをクリア
        for i in range(1, 21):
            setattr(self, f'ingredient_{i}', None)
            setattr(self, f'amount_{i}', None)
            setattr(self, f'unit_{i}', None)
        
        # 新しい材料データを設定
        for i, ingredient in enumerate(ingredients_data[:20], 1):
            setattr(self, f'ingredient_{i}', ingredient.get('name'))
            setattr(self, f'amount_{i}', ingredient.get('amount'))
            setattr(self, f'unit_{i}', ingredient.get('unit'))
    
    def is_existing_recipe(self):
        """既存レシピかどうかを判定"""
        return self.recipe_url is not None
    
    def is_new_recipe(self):
        """新規レシピかどうかを判定"""
        return self.recipe_url is None
    
    def __str__(self):
        return f"{self.recipe_name} by {self.user.username}"


class CookedDish(models.Model):
    """料理履歴モデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  # 直接レシピ参照
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cooked_dishes'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['recipe']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipe.recipe_name} cooked by {self.user.username} at {self.created_at}"


class IngredientCache(models.Model):
    """食材キャッシュモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ingredient_cache'
        unique_together = ['user', 'ingredient_name']
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.ingredient_name} {self.amount}{self.unit} for {self.user.username}"


class ApiKey(models.Model):
    """API Key管理モデル"""
    key_name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'api_keys'
        indexes = [
            models.Index(fields=['api_key']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.key_name} ({'Active' if self.is_active else 'Inactive'})"