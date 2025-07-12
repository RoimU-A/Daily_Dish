# daily_dish/services/line_parser.py
import re
from typing import Dict, List, Tuple, Any
from django.core.exceptions import ValidationError

class LineTextParser:
    """LINEテキスト解析サービス"""
    
    @staticmethod
    def classify_text_type(text: str) -> str:
        """テキストの種類を判定"""
        text = text.strip()
        
        # パターン1: URL（既存レシピ）
        if text.startswith(("http://", "https://")):
            return "url"
        
        # パターン2: ユーザー紐づけ
        if text == "ユーザー紐づけ":
            return "user_linking"
        
        # パターン3: 新規レシピ
        if ("レシピ:" in text and "材料:" in text and "量:" in text):
            return "recipe"
        
        # パターン4: 不明
        return "invalid"
    
    @staticmethod
    def parse_recipe_text(text: str) -> Dict[str, Any]:
        """新規レシピテキストを解析"""
        lines = text.strip().split('\n')
        
        recipe_name = None
        ingredients = []
        amounts = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("レシピ:"):
                recipe_name = line[3:].strip()
            elif line.startswith("材料:"):
                ingredients_str = line[3:].strip()
                ingredients = [ing.strip() for ing in ingredients_str.split("、") if ing.strip()]
            elif line.startswith("量:"):
                amounts_str = line[2:].strip()
                amounts = [amt.strip() for amt in amounts_str.split("、") if amt.strip()]
        
        # バリデーション
        if not recipe_name:
            raise ValidationError("レシピ名が見つかりません")
        if not ingredients:
            raise ValidationError("材料が見つかりません")
        if not amounts:
            raise ValidationError("量が見つかりません")
        if len(ingredients) != len(amounts):
            raise ValidationError(f"材料数({len(ingredients)})と量の数({len(amounts)})が一致しません")
        if len(ingredients) > 20:
            raise ValidationError("材料は最大20個までです")
        
        return {
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "amounts": amounts
        }
    
    @staticmethod
    def parse_amount_and_unit(amount_str: str) -> Tuple[float, str]:
        """量文字列から数値と単位を分離"""
        # 例: "300g" → (300.0, "g"), "1箱" → (1.0, "箱")
        
        # 数値 + 単位のパターン
        match = re.match(r'^(\d+(?:\.\d+)?)\s*(.*)$', amount_str.strip())
        
        if match:
            amount = float(match.group(1))
            unit = match.group(2).strip() or "個"
            return amount, unit
        else:
            # 数値が抽出できない場合はデフォルト値
            return 1.0, amount_str.strip() or "個"
    
    @classmethod
    def create_recipe_data(cls, recipe_name: str, ingredients: List[str], amounts: List[str]) -> Dict[str, Any]:
        """解析結果をRecipeモデル用データに変換"""
        recipe_data = {
            "recipe_name": recipe_name,
            "recipe_url": None  # 新規レシピ
        }
        
        # 材料情報をDBフィールドにマッピング
        ingredients_data = []
        for i, (ingredient, amount_str) in enumerate(zip(ingredients, amounts)):
            if i >= 20:  # 最大20個まで
                break
            
            amount_value, unit = cls.parse_amount_and_unit(amount_str)
            
            # DBフィールド形式
            recipe_data[f'ingredient_{i+1}'] = ingredient
            recipe_data[f'amount_{i+1}'] = amount_value
            recipe_data[f'unit_{i+1}'] = unit
            
            # レスポンス用
            ingredients_data.append({
                'name': ingredient,
                'amount': amount_value,
                'unit': unit
            })
        
        recipe_data['ingredients_data'] = ingredients_data
        return recipe_data