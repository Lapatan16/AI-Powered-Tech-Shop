const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9061';

export const apiClient = {
  async requestAsync<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('auth_token');
    const headers = new Headers(options.headers);

    if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
      headers.set('Content-Type', 'application/json');
    }

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_profile');
      window.location.href = '/login';
      throw new Error('Session expired. Please log in again.');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData?.detail?.error || errorData?.detail || 'API request failed.');
    }

    if (response.status === 204) {
      return null as unknown as T;
    }

    const responseText = await response.text();
    if (!responseText) {
      return null as unknown as T;
    }

    return JSON.parse(responseText) as T;
  }
};