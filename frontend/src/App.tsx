import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LandingPage from './components/LandingPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import DashboardPage from './components/DashboardPage';
import RecipeListPage from './components/RecipeListPage';

// プライベートルートのコンポーネント
const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

// パブリックルートのコンポーネント（認証済みの場合はダッシュボードにリダイレクト）
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Navigate to="/dashboard" /> : <>{children}</>;
};

function AppContent() {
  return (
    <Routes>
      {/* パブリックルート */}
      <Route path="/" element={
        <PublicRoute>
          <LandingPage />
        </PublicRoute>
      } />
      <Route path="/login" element={
        <PublicRoute>
          <LoginPage />
        </PublicRoute>
      } />
      <Route path="/register" element={
        <PublicRoute>
          <RegisterPage />
        </PublicRoute>
      } />
      
      {/* プライベートルート */}
      <Route path="/dashboard" element={
        <PrivateRoute>
          <DashboardPage />
        </PrivateRoute>
      } />
      <Route path="/recipes" element={
        <PrivateRoute>
          <RecipeListPage />
        </PrivateRoute>
      } />
      
      {/* 今後実装予定のルート */}
      <Route path="/recipes/new" element={
        <PrivateRoute>
          <div className="min-h-screen bg-warm-50 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-normal text-stone-800 mb-4">レシピ登録</h2>
              <p className="text-stone-600">実装予定の機能です</p>
            </div>
          </div>
        </PrivateRoute>
      } />
      <Route path="/cooking-history" element={
        <PrivateRoute>
          <div className="min-h-screen bg-warm-50 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-normal text-stone-800 mb-4">料理履歴</h2>
              <p className="text-stone-600">実装予定の機能です</p>
            </div>
          </div>
        </PrivateRoute>
      } />
      <Route path="/shopping-list" element={
        <PrivateRoute>
          <div className="min-h-screen bg-warm-50 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-normal text-stone-800 mb-4">ショッピングリスト</h2>
              <p className="text-stone-600">実装予定の機能です</p>
            </div>
          </div>
        </PrivateRoute>
      } />
      
      {/* 404 ページ */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AppContent />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;