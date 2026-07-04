import React, { useEffect, useState } from 'react';
import { type CategoryTreeModel } from '../../types/category';
import { useAuth } from '../../context/authContext';
import './Header.css';

export const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [categories, setCategories] = useState<CategoryTreeModel[]>([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);

  useEffect(() => {
    const fetchNavigationTree = async () => {
      try {
        const response = await fetch('http://localhost:9061/products/categories/all');
        if (response.ok) setCategories(await response.json());
      } catch (error) {
        console.error('Failed to load menu layers:', error);
      }
    };
    fetchNavigationTree();
  }, []);

  const handleNavigate = (path: string) => {
    window.location.href = path;
  };

  return (
    <header className="main-site-header">
      <div className="header-inner-container">
        <div className="header-left-pane">
          <button className="nav-home-logo-btn" onClick={() => handleNavigate('/')}>
            <span className="logo-accent">E</span>-Store
          </button>
          
          <nav className="header-nav-bar" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div 
              className="categories-menu-wrapper"
              onMouseEnter={() => setIsDropdownOpen(true)}
              onMouseLeave={() => setIsDropdownOpen(false)}
            >
              <button className={`menu-trigger-btn ${isDropdownOpen ? 'active' : ''}`}>
                Categories <span className="chevron-arrow">&#129171;</span>
              </button>

              {isDropdownOpen && categories.length > 0 && (
                <div className="mega-menu-dropdown">
                  <div className="mega-menu-grid">
                    {categories.map((category) => (
                      <div key={category.id} className="mega-menu-column">
                        <h4 className="category-title-link" onClick={() => handleNavigate(`/?category_id=${category.id}`)}>{category.name}</h4>
                        <ul className="subcategory-list">
                          {category.sub_categories.map((sub) => (
                            <li key={sub.id} onClick={() => handleNavigate(`/?sub_category_id=${sub.id}`)}>{sub.name}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {isAuthenticated && (
              <button 
                className="menu-trigger-btn ai-recommendations-btn" 
                onClick={() => handleNavigate('/recommendations')}
                style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                For you
              </button>
            )}
          </nav>
        </div>

        <div className="header-right-pane">
          {isAuthenticated && user ? (
            <div className="profile-badge-hub" style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              
              <button className="header-cart-icon-btn" onClick={() => handleNavigate('/cart')}>
                <span className="cart-graphic-symbol">&#128722;</span> Cart
              </button>

              <button className="profile-avatar-btn" onClick={() => handleNavigate('/dashboard')}>
                <span className="avatar-icon">&#128100;</span> {user.username}
              </button>
              
              <button className="auth-btn btn-secondary" onClick={logout}>
                Logout
              </button>
            </div>
          ) : (
            <div className="auth-btn-group">
              <button className="auth-btn btn-secondary" onClick={() => handleNavigate('/login')}>
                Sign In
              </button>
              <button className="auth-btn btn-primary" onClick={() => handleNavigate('/register')}>
                Register
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;