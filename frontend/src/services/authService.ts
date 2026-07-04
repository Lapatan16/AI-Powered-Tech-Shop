import { jwtDecode } from 'jwt-decode';
import { type AuthResponseModel, type JwtPayloadModel } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9061';

export const authService = {
  async loginAsync(username: string, password: string): Promise<any> {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Invalid username or password configuration.');
    }

    const data: AuthResponseModel = await response.json();
    
    const decoded: JwtPayloadModel = jwtDecode<JwtPayloadModel>(data.access_token);
    
    const userProfile = {
      id: decoded.id,
      username: decoded.sub,
      email: ""
    };

    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('user_profile', JSON.stringify(userProfile));
    
    return {
      access_token: data.access_token,
      user: userProfile
    };
  },

  async registerAsync(username: string, email: string, password: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        user_name: username, 
        email: email, 
        password: password 
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Registration failed.');
    }
  }
};