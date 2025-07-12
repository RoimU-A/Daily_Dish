import React, { useState } from 'react';
import { 
  BookOpenIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  TrashIcon,
  ArrowLeftIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface MockRecipe {
  id: number;
  recipe_name: string;
  recipe_url?: string;
  user: string;
  is_existing_recipe: boolean;
  is_new_recipe: boolean;
  created_at: string;
  updated_at: string;
  ingredients: Array<{
    name: string;
    amount: number;
    unit: string;
  }>;
}

interface RecipeCardProps {
  recipe: MockRecipe;
  onDelete: (id: number) => void;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onDelete }) => {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  const handleDelete = () => {
    onDelete(recipe.id);
    setShowDeleteConfirm(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="bg-white border border-stone-200 p-6 hover:shadow-lg transition-shadow duration-500 group">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-normal text-stone-800 mb-2 tracking-wide group-hover:text-sage-700 transition-colors duration-300">
            {recipe.recipe_name}
          </h3>
          <div className="flex items-center space-x-4 text-sm text-stone-500">
            <span>{formatDate(recipe.created_at)}</span>
            {recipe.recipe_url && (
              <span className="inline-flex items-center px-2 py-1 bg-sage-50 text-sage-700 text-xs rounded">
                既存レシピ
              </span>
            )}
            {!recipe.recipe_url && (
              <span className="inline-flex items-center px-2 py-1 bg-warm-50 text-warm-700 text-xs rounded">
                オリジナル
              </span>
            )}
          </div>
        </div>
        <button
          onClick={() => setShowDeleteConfirm(true)}
          className="w-8 h-8 text-stone-400 hover:text-red-500 transition-colors duration-300 opacity-0 group-hover:opacity-100"
        >
          <TrashIcon className="w-full h-full" />
        </button>
      </div>

      {recipe.ingredients && recipe.ingredients.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-normal text-stone-700 mb-2">材料</h4>
          <div className="flex flex-wrap gap-1">
            {recipe.ingredients.slice(0, 3).map((ingredient, index) => (
              <span 
                key={index}
                className="inline-block px-2 py-1 bg-stone-100 text-stone-600 text-xs rounded"
              >
                {ingredient.name}
              </span>
            ))}
            {recipe.ingredients.length > 3 && (
              <span className="inline-block px-2 py-1 bg-stone-100 text-stone-600 text-xs rounded">
                +{recipe.ingredients.length - 3}個
              </span>
            )}
          </div>
        </div>
      )}

      {recipe.recipe_url && (
        <div className="border-t border-stone-100 pt-4">
          <a
            href={recipe.recipe_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-sage-600 hover:text-sage-700 transition-colors duration-300"
          >
            元のレシピを見る →
          </a>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 max-w-md mx-4 border border-stone-200">
            <div className="flex items-center mb-4">
              <ExclamationTriangleIcon className="w-6 h-6 text-red-500 mr-3" />
              <h3 className="text-lg font-normal text-stone-800">レシピを削除</h3>
            </div>
            <p className="text-stone-600 mb-6 leading-relaxed">
              「{recipe.recipe_name}」を削除しますか？<br />
              この操作は取り消せません。
            </p>
            <div className="flex space-x-4">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="btn-secondary flex-1"
              >
                キャンセル
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 px-6 py-3 bg-red-500 text-white hover:bg-red-600 transition-colors duration-300"
              >
                削除する
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const RecipeListPageDemo: React.FC = () => {
  // モックデータ
  const [recipes, setRecipes] = useState<MockRecipe[]>([
    {
      id: 1,
      recipe_name: "鶏の照り焼き",
      recipe_url: "https://cookpad.com/recipe/12345",
      user: "testuser",
      is_existing_recipe: true,
      is_new_recipe: false,
      created_at: "2024-12-15T10:30:00Z",
      updated_at: "2024-12-15T10:30:00Z",
      ingredients: [
        { name: "鶏もも肉", amount: 300, unit: "g" },
        { name: "醤油", amount: 3, unit: "大さじ" },
        { name: "みりん", amount: 2, unit: "大さじ" },
        { name: "砂糖", amount: 1, unit: "大さじ" },
        { name: "酒", amount: 1, unit: "大さじ" }
      ]
    },
    {
      id: 2,
      recipe_name: "カルボナーラ",
      user: "testuser",
      is_existing_recipe: false,
      is_new_recipe: true,
      created_at: "2024-12-10T14:20:00Z",
      updated_at: "2024-12-10T14:20:00Z",
      ingredients: [
        { name: "パスタ", amount: 200, unit: "g" },
        { name: "ベーコン", amount: 100, unit: "g" },
        { name: "卵", amount: 2, unit: "個" },
        { name: "パルメザンチーズ", amount: 50, unit: "g" }
      ]
    },
    {
      id: 3,
      recipe_name: "味噌汁",
      user: "testuser",
      is_existing_recipe: false,
      is_new_recipe: true,
      created_at: "2024-12-08T09:15:00Z",
      updated_at: "2024-12-08T09:15:00Z",
      ingredients: [
        { name: "味噌", amount: 2, unit: "大さじ" },
        { name: "だしの素", amount: 1, unit: "小さじ" },
        { name: "豆腐", amount: 150, unit: "g" },
        { name: "わかめ", amount: 10, unit: "g" }
      ]
    },
    {
      id: 4,
      recipe_name: "ハンバーグ",
      recipe_url: "https://delishkitchen.tv/recipe/56789",
      user: "testuser",
      is_existing_recipe: true,
      is_new_recipe: false,
      created_at: "2024-12-05T18:45:00Z",
      updated_at: "2024-12-05T18:45:00Z",
      ingredients: [
        { name: "合いびき肉", amount: 400, unit: "g" },
        { name: "玉ねぎ", amount: 1, unit: "個" },
        { name: "パン粉", amount: 50, unit: "g" },
        { name: "卵", amount: 1, unit: "個" },
        { name: "牛乳", amount: 3, unit: "大さじ" }
      ]
    },
    {
      id: 5,
      recipe_name: "チャーハン",
      user: "testuser",
      is_existing_recipe: false,
      is_new_recipe: true,
      created_at: "2024-12-03T12:30:00Z",
      updated_at: "2024-12-03T12:30:00Z",
      ingredients: [
        { name: "ご飯", amount: 300, unit: "g" },
        { name: "卵", amount: 2, unit: "個" },
        { name: "長ねぎ", amount: 1, unit: "本" },
        { name: "ハム", amount: 100, unit: "g" }
      ]
    },
    {
      id: 6,
      recipe_name: "サラダ",
      user: "testuser",
      is_existing_recipe: false,
      is_new_recipe: true,
      created_at: "2024-12-01T16:00:00Z",
      updated_at: "2024-12-01T16:00:00Z",
      ingredients: [
        { name: "レタス", amount: 200, unit: "g" },
        { name: "トマト", amount: 2, unit: "個" },
        { name: "きゅうり", amount: 1, unit: "本" }
      ]
    }
  ]);

  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const recipesPerPage = 4;

  // 検索フィルタリング
  const filteredRecipes = recipes.filter(recipe =>
    recipe.recipe_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // ページネーション計算
  const totalRecipes = filteredRecipes.length;
  const totalPages = Math.ceil(totalRecipes / recipesPerPage);
  const startIndex = (currentPage - 1) * recipesPerPage;
  const endIndex = startIndex + recipesPerPage;
  const currentRecipes = filteredRecipes.slice(startIndex, endIndex);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const handleDelete = (recipeId: number) => {
    setRecipes(prev => prev.filter(recipe => recipe.id !== recipeId));
    alert(`レシピID: ${recipeId} を削除しました（デモ）`);
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleGoBack = () => {
    alert('ダッシュボードに戻る（デモ）');
  };

  const handleNewRecipe = () => {
    alert('新しいレシピ登録ページ（デモ）');
  };

  return (
    <div className="min-h-screen bg-warm-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleGoBack}
                className="w-8 h-8 text-stone-600 hover:text-sage-600 transition-colors duration-300"
              >
                <ArrowLeftIcon className="w-full h-full" />
              </button>
              <h1 className="text-2xl font-normal text-stone-800 tracking-wide">レシピ管理</h1>
            </div>
            <button
              onClick={handleNewRecipe}
              className="btn-primary flex items-center space-x-2"
            >
              <PlusIcon className="w-4 h-4" />
              <span>新しいレシピ</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Search Section */}
        <div className="mb-12">
          <form onSubmit={handleSearch} className="max-w-md mx-auto">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="レシピを検索..."
                className="w-full pl-10 pr-4 py-3 border border-stone-200 bg-white focus:border-sage-300 focus:outline-none transition-colors duration-300"
              />
              <MagnifyingGlassIcon className="w-5 h-5 text-stone-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            </div>
          </form>
        </div>

        {/* Recipe Count */}
        <div className="text-center mb-8">
          <p className="text-stone-600">
            {searchQuery ? `「${searchQuery}」の検索結果: ` : ''}
            {totalRecipes}件のレシピ
          </p>
        </div>

        {/* Recipe Grid */}
        {currentRecipes.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {currentRecipes.map((recipe) => (
                <RecipeCard
                  key={recipe.id}
                  recipe={recipe}
                  onDelete={handleDelete}
                />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-4">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className={`px-4 py-2 border transition-colors duration-300 ${
                    currentPage > 1
                      ? 'border-stone-200 text-stone-600 hover:border-sage-300 hover:text-sage-600'
                      : 'border-stone-100 text-stone-300 cursor-not-allowed'
                  }`}
                >
                  前のページ
                </button>
                <span className="text-stone-600">
                  {currentPage} / {totalPages}ページ
                </span>
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className={`px-4 py-2 border transition-colors duration-300 ${
                    currentPage < totalPages
                      ? 'border-stone-200 text-stone-600 hover:border-sage-300 hover:text-sage-600'
                      : 'border-stone-100 text-stone-300 cursor-not-allowed'
                  }`}
                >
                  次のページ
                </button>
              </div>
            )}
          </>
        ) : (
          /* Empty State */
          <div className="text-center py-16">
            <BookOpenIcon className="w-16 h-16 text-stone-300 mx-auto mb-6" />
            <h3 className="text-xl font-normal text-stone-600 mb-4 tracking-wide">
              {searchQuery ? 'レシピが見つかりませんでした' : 'まだレシピがありません'}
            </h3>
            <p className="text-stone-500 mb-8 leading-relaxed">
              {searchQuery 
                ? '別のキーワードで検索してみてください' 
                : '最初のレシピを登録して、料理の記録を始めましょう'
              }
            </p>
            {!searchQuery && (
              <button
                onClick={handleNewRecipe}
                className="btn-primary"
              >
                レシピを登録する
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeListPageDemo;