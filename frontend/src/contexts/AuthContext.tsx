import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, passwordConfirm: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // APIのベースURL（ローカル開発用）
  const API_BASE = 'http://localhost:8000/api';

  useEffect(() => {
    // ローカルストレージからトークンを復元
    const savedToken = localStorage.getItem('dailydish_token');
    const savedUser = localStorage.getItem('dailydish_user');

    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string): Promise<void> => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/web/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'ログインに失敗しました');
      }

      const data = await response.json();
      
      // ユーザー情報を取得
      const profileResponse = await fetch(`${API_BASE}/web/auth/profile/`, {
        headers: {
          'Authorization': `Bearer ${data.access}`,
          'Content-Type': 'application/json',
        },
      });

      if (!profileResponse.ok) {
        throw new Error('ユーザー情報の取得に失敗しました');
      }

      const userProfile = await profileResponse.json();

      // 状態とローカルストレージを更新
      setToken(data.access);
      setUser(userProfile);
      localStorage.setItem('dailydish_token', data.access);
      localStorage.setItem('dailydish_user', JSON.stringify(userProfile));

    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (username: string, email: string, password: string, passwordConfirm: string): Promise<void> => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/web/auth/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          password_confirm: passwordConfirm,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        
        // エラーメッセージを日本語に変換
        let errorMessage = '登録に失敗しました';
        if (errorData.username) {
          errorMessage = 'このユーザー名は既に使用されています';
        } else if (errorData.email) {
          errorMessage = 'このメールアドレスは既に使用されています';
        } else if (errorData.password) {
          errorMessage = 'パスワードが要件を満たしていません';
        }
        
        throw new Error(errorMessage);
      }

      // 登録成功後、自動的にログイン
      await login(username, password);

    } catch (error) {
      console.error('Register error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (): void => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('dailydish_token');
    localStorage.removeItem('dailydish_user');
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    login,
    register,
    logout,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};