import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  BookOpenIcon, 
  PlusCircleIcon, 
  ClockIcon, 
  ShoppingBagIcon,
  ChartBarIcon,
  CalendarDaysIcon,
  DocumentTextIcon,
  ListBulletIcon
} from '@heroicons/react/24/outline';
import { apiService, type DashboardStats } from '../services/api';

interface StatCardProps {
  icon: React.ReactNode;
  title: string;
  value: string | number;
  description: string;
}

const StatCard: React.FC<StatCardProps> = ({ icon, title, value, description }) => (
  <div className="bg-white border border-stone-200 p-6 hover:shadow-lg transition-shadow duration-500">
    <div className="flex items-center justify-between mb-4">
      <div className="w-10 h-10 text-sage-600">
        {icon}
      </div>
      <div className="text-right">
        <div className="text-2xl font-light text-stone-800 tracking-wide">{value}</div>
      </div>
    </div>
    <h3 className="text-sm font-normal text-stone-700 mb-1 tracking-wide">{title}</h3>
    <p className="text-xs text-stone-500">{description}</p>
  </div>
);

interface ActionButtonProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}

const ActionButton: React.FC<ActionButtonProps> = ({ 
  icon, 
  title, 
  description, 
  onClick 
}) => (
  <button
    onClick={onClick}
    className="bg-white border border-stone-200 p-8 hover:shadow-lg hover:border-sage-300 transition-all duration-500 text-left w-full group"
  >
    <div className="flex items-start space-x-4">
      <div className="w-12 h-12 text-warm-600 group-hover:scale-105 transition-transform duration-300">
        {icon}
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-normal text-stone-800 mb-2 tracking-wide group-hover:text-sage-700 transition-colors duration-300">
          {title}
        </h3>
        <p className="text-stone-600 text-sm leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  </button>
);

const DashboardPage: React.FC = () => {
  const { user, logout, token } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!token) return;
      
      try {
        setIsLoading(true);
        const data = await apiService.getDashboardData(token);
        
        // アカウント作成日からの日数を計算
        const accountDays = user?.id ? 
          Math.floor((Date.now() - new Date('2025-01-01').getTime()) / (1000 * 60 * 60 * 24)) : 0;
        
        setStats({
          total_recipes: data.stats.total_recipes,
          total_cooked_dishes: data.stats.total_cooked_dishes,
          total_ingredient_cache: data.stats.total_ingredient_cache,
          account_days: accountDays
        });
      } catch (err) {
        console.error('Dashboard data fetch error:', err);
        setError('データの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, [token, user]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const mainActions = [
    {
      icon: <BookOpenIcon className="w-full h-full" />,
      title: "レシピ管理",
      description: "登録済みのレシピを確認・編集・削除できます",
      onClick: () => navigate('/recipes')
    },
    {
      icon: <PlusCircleIcon className="w-full h-full" />,
      title: "レシピ登録", 
      description: "新しいレシピを追加してコレクションを充実させます",
      onClick: () => navigate('/recipes/new')
    },
    {
      icon: <ClockIcon className="w-full h-full" />,
      title: "料理履歴",
      description: "過去に作った料理の記録を確認できます",
      onClick: () => navigate('/cooking-history')
    },
    {
      icon: <ShoppingBagIcon className="w-full h-full" />,
      title: "ショッピングリスト",
      description: "必要な材料を管理し、効率的に買い物ができます",
      onClick: () => navigate('/shopping-list')
    }
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-warm-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-sage-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-600">読み込み中...</p>
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
            <h1 className="text-2xl font-normal text-stone-800 tracking-wide">Daily Dish</h1>
            <div className="flex items-center space-x-6">
              <span className="text-stone-600 font-normal">
                {user?.username}さん
              </span>
              <button 
                onClick={handleLogout}
                className="btn-secondary text-sm"
              >
                ログアウト
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Welcome Message */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-light text-stone-800 mb-6 tracking-wide">
            ようこそ、{user?.username}さん
          </h2>
          <p className="text-lg text-stone-600 leading-relaxed">
            今日も素敵な料理を始めましょう
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 mb-8 text-center">
            {error}
          </div>
        )}

        {/* Statistics Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <StatCard
            icon={<DocumentTextIcon className="w-full h-full" />}
            title="登録レシピ"
            value={stats?.total_recipes || 0}
            description="保存されたレシピ数"
          />
          <StatCard
            icon={<ChartBarIcon className="w-full h-full" />}
            title="料理実績"
            value={stats?.total_cooked_dishes || 0}
            description="今月作った料理数"
          />
          <StatCard
            icon={<ListBulletIcon className="w-full h-full" />}
            title="ショッピングリスト"
            value={stats?.total_ingredient_cache || 0}
            description="登録中の材料数"
          />
          <StatCard
            icon={<CalendarDaysIcon className="w-full h-full" />}
            title="利用日数"
            value={stats?.account_days || 0}
            description="アカウント作成から"
          />
        </div>

        {/* Main Actions */}
        <div className="mb-16">
          <h3 className="text-2xl font-light text-stone-800 mb-8 text-center tracking-wide">
            メイン機能
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            {mainActions.map((action, index) => (
              <ActionButton
                key={index}
                icon={action.icon}
                title={action.title}
                description={action.description}
                onClick={action.onClick}
              />
            ))}
          </div>
        </div>

        {/* Quick Tips */}
        <div className="bg-sage-50 border border-sage-200 p-8 text-center">
          <h4 className="text-lg font-normal text-stone-800 mb-4 tracking-wide">
            Daily Dishを始めましょう
          </h4>
          <p className="text-stone-600 leading-relaxed mb-6">
            レシピを登録して、料理の記録を残し、効率的な買い物を楽しみましょう。
          </p>
          <button 
            onClick={() => navigate('/recipes/new')}
            className="btn-primary"
          >
            最初のレシピを登録する
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;