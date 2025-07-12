const API_BASE = 'https://web-production-889e.up.railway.app/api';

export interface DashboardStats {
  total_recipes: number;
  total_cooked_dishes: number;
  total_ingredient_cache: number;
  account_days: number;
}

export interface RecentActivity {
  recent_recipes: Array<{
    id: number;
    recipe_name: string;
    created_at: string;
  }>;
  recent_cooked_dishes: Array<{
    id: number;
    recipe: {
      id: number;
      recipe_name: string;
    };
    created_at: string;
  }>;
}

export interface Recipe {
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

export interface RecipeListResponse {
  count: number;
  next?: string;
  previous?: string;
  results: Recipe[];
}

export const apiService = {
  // 統計情報を取得
  async getDashboardStats(token: string): Promise<DashboardStats> {
    const response = await fetch(`${API_BASE}/web/stats/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('統計情報の取得に失敗しました');
    }

    return response.json();
  },

  // 最近のアクティビティを取得
  async getRecentActivities(token: string): Promise<RecentActivity> {
    const response = await fetch(`${API_BASE}/web/recent-activities/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('最近のアクティビティの取得に失敗しました');
    }

    return response.json();
  },

  // ダッシュボード情報を取得（統合版）
  async getDashboardData(token: string) {
    const response = await fetch(`${API_BASE}/web/dashboard/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('ダッシュボード情報の取得に失敗しました');
    }

    return response.json();
  },

  // レシピ一覧を取得
  async getRecipes(token: string, page?: number, search?: string): Promise<RecipeListResponse> {
    let url = `${API_BASE}/web/recipes/`;
    const params = new URLSearchParams();
    
    if (page && page > 1) {
      params.append('page', page.toString());
    }
    
    if (search) {
      params.append('search', search);
    }
    
    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('レシピ一覧の取得に失敗しました');
    }

    return response.json();
  },

  // 個別レシピを取得
  async getRecipe(token: string, id: number): Promise<Recipe> {
    const response = await fetch(`${API_BASE}/web/recipes/${id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('レシピの取得に失敗しました');
    }

    return response.json();
  },

  // レシピを削除
  async deleteRecipe(token: string, id: number): Promise<void> {
    const response = await fetch(`${API_BASE}/web/recipes/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('レシピの削除に失敗しました');
    }
  },
};