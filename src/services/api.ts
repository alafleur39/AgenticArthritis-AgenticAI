const API_BASE_URL = 'http://localhost:8000';

// Types
export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  age?: number;
  arthritis_type?: string;
  severity_level?: number;
  email_reminders_enabled: boolean;
  reminder_frequency: string;
  preferred_reminder_time: string;
}

export interface Exercise {
  id: number;
  name: string;
  description: string;
  instructions: string;
  target_joints: string;
  difficulty_level: number;
  duration_minutes: number;
  repetitions: number;
  category: string;
  video_url?: string;
  image_url?: string;
  ai_generated: boolean;
  effectiveness_score: number;
}

export interface UserExercise {
  id: number;
  exercise: Exercise;
  custom_repetitions?: number;
  custom_duration?: number;
  difficulty_adjustment: number;
  times_completed: number;
  last_completed?: string;
  is_favorite: boolean;
  is_assigned: boolean;
  average_pain_level?: number;
  average_difficulty?: number;
}

export interface Progress {
  id: number;
  exercise_id?: number;
  exercise_name?: string;
  session_date: string;
  duration_minutes: number;
  repetitions_completed?: number;
  pain_level_before?: number;
  pain_level_after?: number;
  difficulty_rating?: number;
  satisfaction_rating?: number;
  completion_percentage: number;
  notes?: string;
  mood_before?: string;
  mood_after?: string;
  ai_recommendations?: string;
  improvement_detected: boolean;
}

export interface ProgressSummary {
  total_sessions: number;
  total_duration: number;
  average_pain_before: number;
  average_pain_after: number;
  pain_improvement: number;
  average_satisfaction: number;
  consistency_score: number;
  most_effective_exercises: Array<{
    exercise_name: string;
    average_improvement: number;
    sessions: number;
  }>;
  recent_trends: {
    sessions_trend?: number;
    pain_trend?: number;
    satisfaction_trend?: number;
  };
}

export interface AIInsights {
  overall_progress: string;
  pain_trend: string;
  recommendations: string[];
  exercise_adjustments: Array<{
    exercise: string;
    adjustment: string;
    reason: string;
  }>;
  motivational_message: string;
}

export interface Reminder {
  id: number;
  title: string;
  message: string;
  reminder_type: string;
  scheduled_time: string;
  frequency: string;
  is_recurring: boolean;
  is_sent: boolean;
  sent_at?: string;
  is_active: boolean;
  send_email: boolean;
  ai_generated: boolean;
  created_at: string;
}

// API Client Class
class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth methods
  async register(userData: {
    email: string;
    password: string;
    full_name: string;
    age?: number;
    arthritis_type?: string;
    severity_level?: number;
  }): Promise<User> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(email: string, password: string): Promise<{ access_token: string; token_type: string }> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${this.baseURL}/auth/token`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(error.detail || 'Login failed');
    }

    const tokenData = await response.json();
    this.token = tokenData.access_token;
    localStorage.setItem('auth_token', this.token!);
    return tokenData;
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // Exercise methods
  async getExercises(params?: {
    skip?: number;
    limit?: number;
    category?: string;
    difficulty?: number;
  }): Promise<Exercise[]> {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.category) searchParams.append('category', params.category);
    if (params?.difficulty) searchParams.append('difficulty', params.difficulty.toString());

    const query = searchParams.toString();
    return this.request<Exercise[]>(`/exercises${query ? `?${query}` : ''}`);
  }

  async getMyExercises(assignedOnly: boolean = true): Promise<UserExercise[]> {
    return this.request<UserExercise[]>(`/exercises/my-exercises?assigned_only=${assignedOnly}`);
  }

  async assignExercise(exerciseId: number, customization?: {
    custom_repetitions?: number;
    custom_duration?: number;
    difficulty_adjustment?: number;
  }): Promise<UserExercise> {
    return this.request<UserExercise>('/exercises/assign', {
      method: 'POST',
      body: JSON.stringify({
        exercise_id: exerciseId,
        ...customization,
      }),
    });
  }

  async unassignExercise(userExerciseId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/exercises/unassign/${userExerciseId}`, {
      method: 'DELETE',
    });
  }

  async toggleFavorite(userExerciseId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/exercises/favorite/${userExerciseId}`, {
      method: 'POST',
    });
  }

  async generateAIExercises(params: {
    count?: number;
    focus_areas?: string[];
    difficulty_preference?: number;
  }): Promise<any[]> {
    return this.request<any[]>('/exercises/generate', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async getExerciseCategories(): Promise<string[]> {
    return this.request<string[]>('/exercises/categories/list');
  }

  // Progress methods
  async logProgress(progressData: {
    exercise_id?: number;
    duration_minutes: number;
    repetitions_completed?: number;
    pain_level_before?: number;
    pain_level_after?: number;
    difficulty_rating?: number;
    satisfaction_rating?: number;
    completion_percentage?: number;
    notes?: string;
    mood_before?: string;
    mood_after?: string;
  }): Promise<Progress> {
    return this.request<Progress>('/progress/', {
      method: 'POST',
      body: JSON.stringify(progressData),
    });
  }

  async getProgressHistory(params?: {
    skip?: number;
    limit?: number;
    exercise_id?: number;
    days?: number;
  }): Promise<Progress[]> {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.exercise_id) searchParams.append('exercise_id', params.exercise_id.toString());
    if (params?.days) searchParams.append('days', params.days.toString());

    const query = searchParams.toString();
    return this.request<Progress[]>(`/progress${query ? `?${query}` : ''}`);
  }

  async getProgressSummary(days: number = 30): Promise<ProgressSummary> {
    return this.request<ProgressSummary>(`/progress/summary?days=${days}`);
  }

  async getAIInsights(): Promise<AIInsights> {
    return this.request<AIInsights>('/progress/insights');
  }

  async getPainLevelChartData(days: number = 30): Promise<any[]> {
    return this.request<any[]>(`/progress/charts/pain-levels?days=${days}`);
  }

  async getExerciseFrequencyData(days: number = 30): Promise<any[]> {
    return this.request<any[]>(`/progress/charts/exercise-frequency?days=${days}`);
  }

  async getWeeklyProgressData(weeks: number = 12): Promise<any[]> {
    return this.request<any[]>(`/progress/charts/weekly-progress?weeks=${weeks}`);
  }

  // Reminder methods
  async createReminder(reminderData: {
    title: string;
    message: string;
    reminder_type?: string;
    scheduled_time: string;
    is_recurring?: boolean;
    frequency?: string;
    send_email?: boolean;
  }): Promise<Reminder> {
    return this.request<Reminder>('/reminders/', {
      method: 'POST',
      body: JSON.stringify(reminderData),
    });
  }

  async getReminders(params?: {
    skip?: number;
    limit?: number;
    active_only?: boolean;
    reminder_type?: string;
  }): Promise<Reminder[]> {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.active_only !== undefined) searchParams.append('active_only', params.active_only.toString());
    if (params?.reminder_type) searchParams.append('reminder_type', params.reminder_type);

    const query = searchParams.toString();
    return this.request<Reminder[]>(`/reminders${query ? `?${query}` : ''}`);
  }

  async updateReminder(reminderId: number, updates: {
    title?: string;
    message?: string;
    scheduled_time?: string;
    is_active?: boolean;
    send_email?: boolean;
  }): Promise<Reminder> {
    return this.request<Reminder>(`/reminders/${reminderId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteReminder(reminderId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/reminders/${reminderId}`, {
      method: 'DELETE',
    });
  }

  async sendReminderNow(reminderType: string = 'exercise'): Promise<{ message: string }> {
    return this.request<{ message: string }>('/reminders/send-now', {
      method: 'POST',
      body: JSON.stringify({ reminder_type: reminderType }),
    });
  }

  async scheduleDailyReminders(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/reminders/schedule-daily', {
      method: 'POST',
    });
  }

  async updateReminderPreferences(preferences: {
    email_reminders_enabled: boolean;
    reminder_frequency: string;
    preferred_reminder_time: string;
  }): Promise<{ message: string }> {
    return this.request<{ message: string }>('/reminders/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    });
  }

  async getReminderPreferences(): Promise<{
    email_reminders_enabled: boolean;
    reminder_frequency: string;
    preferred_reminder_time: string;
  }> {
    return this.request('/reminders/preferences/current');
  }

  async getReminderStats(days: number = 30): Promise<any> {
    return this.request(`/reminders/stats/summary?days=${days}`);
  }

  // Health check
  async healthCheck(): Promise<any> {
    return this.request('/health');
  }
}

// Export singleton instance
export const apiClient = new ApiClient(API_BASE_URL);

// Export individual methods for convenience
export const {
  register,
  login,
  getCurrentUser,
  logout,
  getExercises,
  getMyExercises,
  assignExercise,
  unassignExercise,
  toggleFavorite,
  generateAIExercises,
  getExerciseCategories,
  logProgress,
  getProgressHistory,
  getProgressSummary,
  getAIInsights,
  getPainLevelChartData,
  getExerciseFrequencyData,
  getWeeklyProgressData,
  createReminder,
  getReminders,
  updateReminder,
  deleteReminder,
  sendReminderNow,
  scheduleDailyReminders,
  updateReminderPreferences,
  getReminderPreferences,
  getReminderStats,
  healthCheck,
} = apiClient;