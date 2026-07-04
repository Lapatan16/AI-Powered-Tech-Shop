import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import { useAuth } from '../../context/authContext';
import './AuthPage.css';

export const AuthPage: React.FC = () => {
  const { login } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const [isLoginMode, setIsLoginMode] = useState<boolean>(location.pathname === '/login');
  
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    setIsLoginMode(location.pathname === '/login');
    setErrorMessage(null);
    setSuccessMessage(null);
  }, [location.pathname]);

  const handleModeToggle = () => {
    const targetPath = isLoginMode ? '/register' : '/login';
    navigate(targetPath);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      setIsLoading(true);
      if (isLoginMode) {
        const response = await authService.loginAsync(username, password);
        
        login(response.access_token, response.user);
        
        setSuccessMessage('Logged in successfully! Redirecting...');
        setTimeout(() => { window.location.href = '/'; }, 1000);
      } else {
        await authService.registerAsync(username, email, password);
        setSuccessMessage('Account created! Shifting to sign in...');
        setTimeout(() => { setIsLoginMode(true); }, 1500);
      }
    } catch (err: any) {
      setErrorMessage('An error occurred. Please check your credentials and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="auth-page-container">
      <div className="auth-card-panel">
        <header className="auth-card-header">
          <h2>{isLoginMode ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{isLoginMode ? 'Sign in to manage your cart and view updates' : 'Join our store platform to check items out'}</p>
        </header>

        {errorMessage && (
          <div className="auth-status-alert alert-danger" role="alert">
            <span>⚠️</span> {errorMessage}
          </div>
        )}

        {successMessage && (
          <div className="auth-status-alert alert-success" role="alert">
            <span>✓</span> {successMessage}
          </div>
        )}

        <form className="auth-form-body" onSubmit={handleSubmit}>
          <div className="form-input-group">
            <label htmlFor="username-field">Username</label>
            <input
              id="username-field"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your system username"
              disabled={isLoading}
              required
            />
          </div>

          {!isLoginMode && (
            <div className="form-input-group">
              <label htmlFor="email-field">Email Address</label>
              <input
                id="email-field"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                disabled={isLoading}
                required
              />
            </div>
          )}

          <div className="form-input-group">
            <label htmlFor="password-field">Password</label>
            <input
              id="password-field"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={isLoading}
              required
            />
          </div>

          {!isLoginMode && (
            <div className="form-input-group">
              <label htmlFor="confirm-password-field">Confirm Password</label>
              <input
                id="confirm-password-field"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                disabled={isLoading}
                required
              />
            </div>
          )}

          <button className="auth-submit-cta" type="submit" disabled={isLoading}>
            {isLoading ? <div className="button-spinner"></div> : isLoginMode ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <footer className="auth-card-footer">
            <p>
                {isLoginMode ? "Don't have an account yet?" : 'Already a registered store partner?'}
                <button type="button" className="switch-mode-btn" onClick={handleModeToggle} disabled={isLoading}>
                    {isLoginMode ? 'Register here' : 'Sign in here'}
                </button>
            </p>
        </footer>
      </div>
    </main>
  );
};

export default AuthPage;