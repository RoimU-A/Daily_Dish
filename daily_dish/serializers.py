from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Recipe, CookedDish, IngredientCache, ApiKey

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ユーザーシリアライザー"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """ユーザー作成用シリアライザー"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("パスワードが一致しません")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class RecipeSerializer(serializers.ModelSerializer):
    """統一レシピシリアライザー"""
    ingredients = serializers.SerializerMethodField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    is_existing_recipe = serializers.BooleanField(read_only=True)
    is_new_recipe = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'user', 'recipe_name', 'recipe_url', 'ingredients', 
                 'is_existing_recipe', 'is_new_recipe', 'created_at', 'updated_at'] + \
                [f'ingredient_{i}' for i in range(1, 21)] + \
                [f'amount_{i}' for i in range(1, 21)] + \
                [f'unit_{i}' for i in range(1, 21)]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_ingredients(self, obj):
        """材料リストを取得"""
        return obj.get_ingredients()
    
    def create(self, validated_data):
        """レシピ作成時にユーザーを自動設定"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        """レシピのバリデーション"""
        # 最低1つの材料は必要
        has_ingredient = False
        for i in range(1, 21):
            name = attrs.get(f'ingredient_{i}')
            amount = attrs.get(f'amount_{i}')
            unit = attrs.get(f'unit_{i}')
            
            if name and amount and unit:
                has_ingredient = True
                break
        
        if not has_ingredient:
            raise serializers.ValidationError('最低1つの材料は必要です')
        
        return attrs


class CookedDishSerializer(serializers.ModelSerializer):
    """料理履歴シリアライザー"""
    user = serializers.StringRelatedField(read_only=True)
    recipe_detail = RecipeSerializer(source='recipe', read_only=True)
    
    class Meta:
        model = CookedDish
        fields = ['id', 'user', 'recipe', 'recipe_detail', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """料理履歴作成時にユーザーを自動設定"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_recipe(self, value):
        """レシピの所有者チェック"""
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError('他のユーザーのレシピは使用できません')
        return value


class IngredientCacheSerializer(serializers.ModelSerializer):
    """食材キャッシュシリアライザー"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = IngredientCache
        fields = ['id', 'user', 'ingredient_name', 'amount', 'unit', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """食材キャッシュ作成時にユーザーを自動設定"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ApiKeySerializer(serializers.ModelSerializer):
    """API Key表示用シリアライザー（管理用）"""
    
    class Meta:
        model = ApiKey
        fields = ['id', 'key_name', 'is_active', 'created_at', 'expires_at', 
                 'last_used_at', 'usage_count']
        read_only_fields = ['id', 'created_at', 'last_used_at', 'usage_count']


# 外部アプリ向けのシンプルなシリアライザー
class ExternalRecipeSerializer(serializers.ModelSerializer):
    """外部アプリ向けレシピシリアライザー"""
    ingredients = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name', 'recipe_url', 'ingredients', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_ingredients(self, obj):
        return obj.get_ingredients()


class ExternalCookedDishSerializer(serializers.ModelSerializer):
    """外部アプリ向け料理履歴シリアライザー"""
    recipe_name = serializers.CharField(source='recipe.recipe_name', read_only=True)
    
    class Meta:
        model = CookedDish
        fields = ['id', 'recipe_name', 'created_at']
        read_only_fields = ['id', 'recipe_name', 'created_at']


class ExternalIngredientCacheSerializer(serializers.ModelSerializer):
    """外部アプリ向け食材キャッシュシリアライザー"""
    
    class Meta:
        model = IngredientCache
        fields = ['id', 'ingredient_name', 'amount', 'unit', 'created_at']
        read_only_fields = ['id', 'created_at']