import React, { createContext, useContext, useState, useEffect } from 'react';

interface UserProfile {
  id: number;
  email: string;
  username: string;
}

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  login: (token: string, user: UserProfile) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    const cachedUser = localStorage.getItem('user_profile');
    const cachedToken = localStorage.getItem('auth_token');
    if (cachedUser && cachedToken) {
      setUser(JSON.parse(cachedUser));
    }
  }, []);

  const login = (token: string, userProfile: UserProfile) => {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_profile', JSON.stringify(userProfile));
    setUser(userProfile);
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_profile');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};