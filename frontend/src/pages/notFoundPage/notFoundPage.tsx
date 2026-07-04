import React from 'react';
import { useNavigate } from 'react-router-dom';
import './notFoundPage.css';

export const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <main className="not-found-container">
      <div className="not-found-content">
        <div className="error-code-badge">404</div>
        
        <header className="not-found-header">
          <h1>Page Not Found</h1>
          <p>
            The tech specifications or inventory collection layer you are looking for 
            does not exist, has been rotated out of catalog bounds, or moved permanently.
          </p>
        </header>

        <div className="not-found-actions">
          <button className="nav-cta btn-primary" onClick={() => navigate('/')}>
            &larr; Return to Main Catalog
          </button>
          <button className="nav-cta btn-secondary" onClick={() => navigate(-1)}>
            Go Back
          </button>
        </div>
      </div>
    </main>
  );
};

export default NotFoundPage;