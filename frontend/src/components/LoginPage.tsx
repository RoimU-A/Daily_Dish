import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface LoginFormData {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<LoginFormData>({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login(formData.username, formData.password);
      // ログイン成功時は自動的にダッシュボードにリダイレクトされる
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ログインに失敗しました。ユーザー名とパスワードを確認してください。');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-warm-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-normal text-stone-800 tracking-wide">Daily Dish</h1>
            <div className="space-x-6">
              <button 
                onClick={() => navigate('/')}
                className="text-stone-600 hover:text-stone-800 font-normal transition-colors duration-300"
              >
                ホームに戻る
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="max-w-md w-full">
          {/* Title */}
          <div className="text-center mb-12">
            <h2 className="text-3xl font-light text-stone-800 mb-4 tracking-wide">
              ログイン
            </h2>
            <p className="text-stone-600 leading-relaxed">
              Daily Dishへようこそ。<br />
              アカウントにログインしてください。
            </p>
          </div>

          {/* Login Form */}
          <div className="bg-white border border-stone-200 p-8 shadow-sm">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Username Field */}
              <div>
                <label 
                  htmlFor="username" 
                  className="block text-sm font-normal text-stone-700 mb-2 tracking-wide"
                >
                  ユーザー名またはメールアドレス
                </label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-stone-300 bg-white text-stone-800 placeholder-stone-400 focus:border-sage-400 focus:outline-none transition-colors duration-300"
                  placeholder="ユーザー名またはメールアドレスを入力"
                />
              </div>

              {/* Password Field */}
              <div>
                <label 
                  htmlFor="password" 
                  className="block text-sm font-normal text-stone-700 mb-2 tracking-wide"
                >
                  パスワード
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 pr-12 border border-stone-300 bg-white text-stone-800 placeholder-stone-400 focus:border-sage-400 focus:outline-none transition-colors duration-300"
                    placeholder="パスワードを入力"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-600 transition-colors duration-200"
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="w-5 h-5" />
                    ) : (
                      <EyeIcon className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-sage-600 hover:bg-sage-700 disabled:bg-sage-400 text-white font-normal py-3 px-6 border border-sage-600 hover:border-sage-700 disabled:border-sage-400 transition-all duration-300"
              >
                {isLoading ? 'ログイン中...' : 'ログイン'}
              </button>
            </form>

            {/* Forgot Password */}
            <div className="mt-6 text-center">
              <button className="text-stone-600 hover:text-stone-800 text-sm font-normal transition-colors duration-300">
                パスワードをお忘れですか？
              </button>
            </div>
          </div>

          {/* Register Link */}
          <div className="mt-8 text-center">
            <p className="text-stone-600 text-sm mb-4">
              アカウントをお持ちでない方
            </p>
            <button 
              onClick={() => navigate('/register')}
              className="btn-secondary w-full"
            >
              新規登録
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-stone-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="text-center">
            <p className="text-stone-400 text-sm">© 2025 Daily Dish. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LoginPage;