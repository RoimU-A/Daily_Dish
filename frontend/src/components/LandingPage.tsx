import React from 'react';
import { BookOpenIcon, HeartIcon, ShoppingBagIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';

interface FeatureProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const Feature: React.FC<FeatureProps> = ({ icon, title, description }) => (
  <div className="text-center py-12">
    <div className="flex justify-center mb-6">
      <div className="w-12 h-12 text-sage-600">
        {icon}
      </div>
    </div>
    <h3 className="text-xl font-normal text-stone-800 mb-4 tracking-wide">{title}</h3>
    <p className="text-stone-600 leading-relaxed max-w-sm mx-auto">{description}</p>
  </div>
);

const RecipeCard: React.FC<{ name: string; description: string }> = ({ name, description }) => (
  <div className="bg-white border border-stone-200 p-8 hover:shadow-lg transition-shadow duration-500">
    <h4 className="text-lg font-normal text-stone-800 mb-3 tracking-wide">{name}</h4>
    <p className="text-stone-600 text-sm leading-relaxed">{description}</p>
  </div>
);

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const features = [
    {
      icon: <BookOpenIcon className="w-full h-full" />,
      title: "レシピ管理",
      description: "お気に入りのレシピを美しく整理し、いつでも簡単にアクセスできます。"
    },
    {
      icon: <HeartIcon className="w-full h-full" />,
      title: "料理記録",
      description: "作った料理の思い出を記録し、あなたの料理の歴史を残します。"
    },
    {
      icon: <ShoppingBagIcon className="w-full h-full" />,
      title: "買い物リスト",
      description: "必要な材料を自動で整理し、効率的な買い物をサポートします。"
    }
  ];

  const sampleRecipes = [
    { name: "季節の野菜炒め", description: "旬の野菜を使ったシンプルで健康的な一品" },
    { name: "手作りパスタ", description: "丁寧に作る本格的なイタリアンパスタ" },
    { name: "和風ハンバーグ", description: "日本の家庭の味を大切にした優しい味わい" },
    { name: "季節のスープ", description: "体に優しく心温まる滋養豊かなスープ" }
  ];

  return (
    <div className="min-h-screen bg-warm-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-normal text-stone-800 tracking-wide">Daily Dish</h1>
            <div className="space-x-6">
              <button 
                onClick={() => navigate('/login')}
                className="btn-secondary text-sm"
              >
                ログイン
              </button>
              <button 
                onClick={() => navigate('/register')}
                className="btn-primary text-sm"
              >
                新規登録
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-light text-stone-800 mb-8 leading-tight tracking-wide">
            毎日の料理を<br />
            もっと心地よく
          </h2>
          <p className="text-lg text-stone-600 mb-12 leading-relaxed max-w-2xl mx-auto">
            Daily Dishは、あなたの料理ライフを静かにサポートします。<br />
            レシピの管理から買い物まで、シンプルで美しい体験を。
          </p>
          <div className="space-y-4 sm:space-y-0 sm:space-x-6 sm:flex sm:justify-center">
            <button 
              onClick={() => navigate('/register')}
              className="btn-primary block sm:inline-block"
            >
              今すぐ始める
            </button>
            <button className="btn-secondary block sm:inline-block">詳しく見る</button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-light text-stone-800 mb-6 tracking-wide">
              シンプルな機能
            </h3>
            <p className="text-stone-600 leading-relaxed max-w-2xl mx-auto">
              料理に必要な機能だけを、美しく使いやすい形でご提供します。
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-12">
            {features.map((feature, index) => (
              <Feature
                key={index}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Sample Recipes */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-light text-stone-800 mb-6 tracking-wide">
              料理の記録
            </h3>
            <p className="text-stone-600 leading-relaxed max-w-2xl mx-auto">
              あなたの大切なレシピと料理の思い出を、美しく整理して保存できます。
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {sampleRecipes.map((recipe, index) => (
              <RecipeCard
                key={index}
                name={recipe.name}
                description={recipe.description}
              />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-sage-50">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h3 className="text-3xl font-light text-stone-800 mb-8 tracking-wide">
            料理をもっと楽しく
          </h3>
          <p className="text-lg text-stone-600 mb-12 leading-relaxed">
            今すぐDaily Dishを始めて、<br />
            あなたの料理ライフを豊かにしませんか。
          </p>
          <button 
            onClick={() => navigate('/register')}
            className="btn-primary"
          >
            無料で始める
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="text-center">
            <h4 className="text-xl font-normal text-stone-800 mb-4 tracking-wide">Daily Dish</h4>
            <p className="text-stone-500 mb-6">毎日の料理をもっと心地よく</p>
            <p className="text-stone-400 text-sm">© 2025 Daily Dish. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;