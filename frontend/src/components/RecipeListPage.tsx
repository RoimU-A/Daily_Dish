import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  BookOpenIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  TrashIcon,
  ArrowLeftIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { apiService, type Recipe, type RecipeListResponse } from '../services/api';

interface RecipeCardProps {
  recipe: Recipe;
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

const RecipeListPage: React.FC = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);

  const fetchRecipes = async (page: number = 1, search: string = '') => {
    if (!token) return;
    
    try {
      setIsLoading(true);
      setError('');
      const response: RecipeListResponse = await apiService.getRecipes(
        token, 
        page,
        search || undefined
      );
      
      setRecipes(response.results);
      setTotalCount(response.count);
      setHasNext(!!response.next);
      setHasPrevious(!!response.previous);
      setCurrentPage(page);
    } catch (err) {
      console.error('Recipe fetch error:', err);
      setError('レシピの取得に失敗しました');
      setRecipes([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRecipes(1, searchQuery);
  }, [token]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchRecipes(1, searchQuery);
  };

  const handleDelete = async (recipeId: number) => {
    if (!token) return;
    
    try {
      await apiService.deleteRecipe(token, recipeId);
      // レシピリストを再取得
      fetchRecipes(currentPage, searchQuery);
    } catch (err) {
      console.error('Recipe delete error:', err);
      setError('レシピの削除に失敗しました');
    }
  };

  const handlePageChange = (newPage: number) => {
    fetchRecipes(newPage, searchQuery);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-warm-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-sage-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-600">レシピを読み込み中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-warm-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="w-8 h-8 text-stone-600 hover:text-sage-600 transition-colors duration-300"
              >
                <ArrowLeftIcon className="w-full h-full" />
              </button>
              <h1 className="text-2xl font-normal text-stone-800 tracking-wide">レシピ管理</h1>
            </div>
            <button
              onClick={() => navigate('/recipes/new')}
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

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 mb-8 text-center">
            {error}
          </div>
        )}

        {/* Recipe Count */}
        {!isLoading && (
          <div className="text-center mb-8">
            <p className="text-stone-600">
              {searchQuery ? `「${searchQuery}」の検索結果: ` : ''}
              {totalCount}件のレシピ
            </p>
          </div>
        )}

        {/* Recipe Grid */}
        {recipes.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {recipes.map((recipe) => (
                <RecipeCard
                  key={recipe.id}
                  recipe={recipe}
                  onDelete={handleDelete}
                />
              ))}
            </div>

            {/* Pagination */}
            {(hasNext || hasPrevious) && (
              <div className="flex justify-center items-center space-x-4">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={!hasPrevious}
                  className={`px-4 py-2 border transition-colors duration-300 ${
                    hasPrevious
                      ? 'border-stone-200 text-stone-600 hover:border-sage-300 hover:text-sage-600'
                      : 'border-stone-100 text-stone-300 cursor-not-allowed'
                  }`}
                >
                  前のページ
                </button>
                <span className="text-stone-600">
                  {currentPage}ページ
                </span>
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={!hasNext}
                  className={`px-4 py-2 border transition-colors duration-300 ${
                    hasNext
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
                onClick={() => navigate('/recipes/new')}
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

export default RecipeListPage;