import React from 'react';
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

const DashboardPageDemo: React.FC = () => {
  // モックデータ
  const mockUser = { username: "サンプルユーザー" };
  const mockStats = {
    total_recipes: 12,
    total_cooked_dishes: 35,
    total_ingredient_cache: 8,
    account_days: 28
  };

  const handleLogout = () => {
    alert('ログアウト機能（デモ）');
  };

  const mainActions = [
    {
      icon: <BookOpenIcon className="w-full h-full" />,
      title: "レシピ管理",
      description: "登録済みのレシピを確認・編集・削除できます",
      onClick: () => alert('レシピ管理ページ（デモ）')
    },
    {
      icon: <PlusCircleIcon className="w-full h-full" />,
      title: "レシピ登録", 
      description: "新しいレシピを追加してコレクションを充実させます",
      onClick: () => alert('レシピ登録ページ（デモ）')
    },
    {
      icon: <ClockIcon className="w-full h-full" />,
      title: "料理履歴",
      description: "過去に作った料理の記録を確認できます",
      onClick: () => alert('料理履歴ページ（デモ）')
    },
    {
      icon: <ShoppingBagIcon className="w-full h-full" />,
      title: "ショッピングリスト",
      description: "必要な材料を管理し、効率的に買い物ができます",
      onClick: () => alert('ショッピングリストページ（デモ）')
    }
  ];

  return (
    <div className="min-h-screen bg-warm-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-normal text-stone-800 tracking-wide">Daily Dish</h1>
            <div className="flex items-center space-x-6">
              <span className="text-stone-600 font-normal">
                {mockUser.username}さん
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
            ようこそ、{mockUser.username}さん
          </h2>
          <p className="text-lg text-stone-600 leading-relaxed">
            今日も素敵な料理を始めましょう
          </p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <StatCard
            icon={<DocumentTextIcon className="w-full h-full" />}
            title="登録レシピ"
            value={mockStats.total_recipes}
            description="保存されたレシピ数"
          />
          <StatCard
            icon={<ChartBarIcon className="w-full h-full" />}
            title="料理実績"
            value={mockStats.total_cooked_dishes}
            description="今月作った料理数"
          />
          <StatCard
            icon={<ListBulletIcon className="w-full h-full" />}
            title="ショッピングリスト"
            value={mockStats.total_ingredient_cache}
            description="登録中の材料数"
          />
          <StatCard
            icon={<CalendarDaysIcon className="w-full h-full" />}
            title="利用日数"
            value={mockStats.account_days}
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
            onClick={() => alert('レシピ登録ページ（デモ）')}
            className="btn-primary"
          >
            最初のレシピを登録する
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPageDemo;