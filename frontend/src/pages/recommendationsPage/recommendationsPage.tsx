import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { type ProductMinimalModel } from '../../types/product';
import { productService } from '../../services/productService';
import { ProductGrid } from '../../components/productGrid/productGrid';
import './recommendationsPage.css';

export const RecommendationsPage: React.FC = () => {
  const navigate = useNavigate();

  const [products, setProducts] = useState<ProductMinimalModel[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAIRecommendations = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data = await productService.getAIRecommendationsAsync();
        
        setProducts(data || []);
      } catch (err: any) {
        setError(err.message || 'Something went wrong while compiling your personalized tech catalog.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAIRecommendations();
  }, []);

  const handleNavigateToCatalog = () => {
    navigate('/');
  };

  return (
    <main className="recommendations-page-main-div">
      <header className="recommendations-page-header">
        <h1>Products for you</h1>
        <p>Tailored accessory upgrades analyzed directly from your shopping trends</p>
      </header>

      {isLoading && (
        <div className="home-page-status-message msg-loading">
          <div className="spinner"></div>
          <p>Analyzing purchase records and building your smart catalog...</p>
        </div>
      )}

      {!isLoading && error && (
        <div className="home-page-status-message msg-error">
          <p>⚠️ Error compiling recommendation profile: {error}</p>
          <button onClick={() => window.location.reload()}>Retry Sync</button>
        </div>
      )}

      {!isLoading && !error && products.length === 0 && (
        <div className="home-page-status-message msg-empty">
          <p>Our Gemini model hasn't generated your companion catalog profile yet.</p>
          <p className="sub-text-hint">Complete a checkout order to activate your custom recommendation suggestions.</p>
          <button onClick={handleNavigateToCatalog}>Explore Store Items</button>
        </div>
      )}

      {!isLoading && !error && products.length > 0 && (
        <div className="recommendations-grid-container">
          <ProductGrid 
            products={products} 
            onProductClick={(id) => navigate(`/products/${id}`)} 
          />
        </div>
      )}
    </main>
  );
};

export default RecommendationsPage;