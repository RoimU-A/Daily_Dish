import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  passwordConfirm: string;
}

interface PasswordValidation {
  length: boolean;
  match: boolean;
}

const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: '',
    passwordConfirm: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const passwordValidation: PasswordValidation = {
    length: formData.password.length >= 8,
    match: formData.password === formData.passwordConfirm && formData.passwordConfirm.length > 0
  };

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

    // Validation
    if (!passwordValidation.length) {
      setError('パスワードは8文字以上で入力してください。');
      setIsLoading(false);
      return;
    }

    if (!passwordValidation.match) {
      setError('パスワードが一致しません。');
      setIsLoading(false);
      return;
    }

    try {
      await register(formData.username, formData.email, formData.password, formData.passwordConfirm);
      // 登録成功時は自動的にダッシュボードにリダイレクトされる
    } catch (err) {
      setError(err instanceof Error ? err.message : '登録に失敗しました。入力内容を確認してください。');
    } finally {
      setIsLoading(false);
    }
  };

  const ValidationIcon: React.FC<{ isValid: boolean }> = ({ isValid }) => (
    isValid ? (
      <CheckCircleIcon className="w-4 h-4 text-sage-600" />
    ) : (
      <XCircleIcon className="w-4 h-4 text-stone-400" />
    )
  );

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
              新規登録
            </h2>
            <p className="text-stone-600 leading-relaxed">
              Daily Dishのアカウントを作成して、<br />
              料理ライフを始めましょう。
            </p>
          </div>

          {/* Register Form */}
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
                  ユーザー名
                </label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-stone-300 bg-white text-stone-800 placeholder-stone-400 focus:border-sage-400 focus:outline-none transition-colors duration-300"
                  placeholder="ユーザー名を入力"
                />
              </div>

              {/* Email Field */}
              <div>
                <label 
                  htmlFor="email" 
                  className="block text-sm font-normal text-stone-700 mb-2 tracking-wide"
                >
                  メールアドレス
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-stone-300 bg-white text-stone-800 placeholder-stone-400 focus:border-sage-400 focus:outline-none transition-colors duration-300"
                  placeholder="メールアドレスを入力"
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

              {/* Password Confirmation Field */}
              <div>
                <label 
                  htmlFor="passwordConfirm" 
                  className="block text-sm font-normal text-stone-700 mb-2 tracking-wide"
                >
                  パスワード確認
                </label>
                <div className="relative">
                  <input
                    type={showPasswordConfirm ? 'text' : 'password'}
                    id="passwordConfirm"
                    name="passwordConfirm"
                    value={formData.passwordConfirm}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 pr-12 border border-stone-300 bg-white text-stone-800 placeholder-stone-400 focus:border-sage-400 focus:outline-none transition-colors duration-300"
                    placeholder="パスワードを再度入力"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-600 transition-colors duration-200"
                  >
                    {showPasswordConfirm ? (
                      <EyeSlashIcon className="w-5 h-5" />
                    ) : (
                      <EyeIcon className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Password Validation */}
              {formData.password && (
                <div className="bg-stone-50 p-4 space-y-2">
                  <p className="text-sm font-normal text-stone-700 mb-2">パスワード要件</p>
                  <div className="flex items-center space-x-2 text-sm">
                    <ValidationIcon isValid={passwordValidation.length} />
                    <span className={passwordValidation.length ? 'text-sage-700' : 'text-stone-500'}>
                      8文字以上
                    </span>
                  </div>
                  {formData.passwordConfirm && (
                    <div className="flex items-center space-x-2 text-sm">
                      <ValidationIcon isValid={passwordValidation.match} />
                      <span className={passwordValidation.match ? 'text-sage-700' : 'text-stone-500'}>
                        パスワードが一致
                      </span>
                    </div>
                  )}
                </div>
              )}

              {/* Register Button */}
              <button
                type="submit"
                disabled={isLoading || !passwordValidation.length || !passwordValidation.match}
                className="w-full bg-sage-600 hover:bg-sage-700 disabled:bg-sage-400 text-white font-normal py-3 px-6 border border-sage-600 hover:border-sage-700 disabled:border-sage-400 transition-all duration-300"
              >
                {isLoading ? '登録中...' : 'アカウントを作成'}
              </button>
            </form>

            {/* Terms */}
            <div className="mt-6 text-center">
              <p className="text-stone-500 text-xs leading-relaxed">
                アカウント作成により、
                <button className="text-sage-600 hover:text-sage-700 underline transition-colors duration-300">
                  利用規約
                </button>
                および
                <button className="text-sage-600 hover:text-sage-700 underline transition-colors duration-300">
                  プライバシーポリシー
                </button>
                に同意したものとみなされます。
              </p>
            </div>
          </div>

          {/* Login Link */}
          <div className="mt-8 text-center">
            <p className="text-stone-600 text-sm mb-4">
              すでにアカウントをお持ちの方
            </p>
            <button 
              onClick={() => navigate('/login')}
              className="btn-secondary w-full"
            >
              ログイン
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

export default RegisterPage;