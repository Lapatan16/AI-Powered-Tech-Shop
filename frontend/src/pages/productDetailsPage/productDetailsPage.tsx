import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { type ProductDetailModel } from '../../types/product';
import { productService } from '../../services/productService';
import { cartService } from '../../services/cartService';
import { useAuth } from '../../context/authContext';
import { ImageGallery } from '../../components/imageGallery/imageGallery';
import './productDetailsPage.css';

interface ProductDetailPageProps {
  productId?: number; 
}

const ProductDetailPage: React.FC<ProductDetailPageProps> = ({ productId }) => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  
  const resolvedId = productId || parseInt(window.location.pathname.split('/').pop() || '0', 10);

  const [product, setProduct] = useState<ProductDetailModel | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [quantity, setQuantity] = useState<number>(1);

  useEffect(() => {
    if (!resolvedId) {
      setError('Invalid system context reference ID lookup configuration.');
      setIsLoading(false);
      return;
    }

    const loadProductProfile = async () => {
      try {
        setIsLoading(true);
        const data = await productService.getProductByIdAsync(resolvedId);
        setProduct(data);
      } catch (err: any) {
        setError(err.message || 'Error pulling selected merchandise layout records.');
      } finally {
        setIsLoading(false);
      }
    };

    loadProductProfile();
  }, [resolvedId]);

  const handleAddToCart = async () => {
    if (!product) return;

    if (!isAuthenticated) {
      alert('Authentication required. Please sign in to add items to your cart.');
      navigate('/login');
      return;
    }

    try {
      setIsSubmitting(true);
      
      await cartService.addProductToCartAsync(product.id, quantity);
      
      alert(`Success: Added ${quantity} unit(s) of "${product.name}" to your cart!`);
    } catch (err: any) {
      alert(err.message || 'Failed to sync item addition with your cart profile.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="detail-status-view">
        <div className="spinner"></div>
        <p>Loading explicit item specifications...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="detail-status-view error-layout">
        <p>⚠️ Error: {error || 'Product data structure error profile missing context.'}</p>
        <button onClick={() => navigate(-1)}>Return to Main Catalog</button>
      </div>
    );
  }

  const hasDiscount = product.discount > 0;
  const finalPrice = hasDiscount ? product.price * (1 - product.discount / 100) : product.price;
  const isOutOfStock = product.stock <= 0;

  return (
    <main className="product-detail-container">
      <nav className="detail-breadcrumb">
        <button onClick={() => navigate(-1)}>&larr; Back to Catalog Listings</button>
      </nav>

      <div className="product-detail-layout">
        <section className="detail-media-pane">
          <ImageGallery images={product.images} productName={product.name} />
        </section>

        <section className="detail-info-pane">
          <header className="detail-header-block">
            <h1 className="detail-main-title">{product.name}</h1>
            <span className="stock-pill-badge" data-instock={!isOutOfStock}>
              {isOutOfStock ? 'Sold Out' : `In Stock (${product.stock} left)`}
            </span>
          </header>

          <hr className="divider-bar" />

          <div className="detail-pricing-panel">
            {hasDiscount ? (
              <div className="detail-price-stack">
                <div className="deal-incentive-header">
                  <span className="percentage-pill">-{product.discount}% OFF</span>
                  <span className="retail-strike">${product.price.toFixed(2)} MSRP</span>
                </div>
                <div className="active-deal-price">${finalPrice.toFixed(2)}</div>
              </div>
            ) : (
              <div className="active-deal-price">${product.price.toFixed(2)}</div>
            )}
          </div>

          <p className="detail-text-description">{product.description}</p>

          <hr className="divider-bar" />

          {!isOutOfStock && (
            <div className="purchase-controls-block">
              <div className="quantity-selector-rack">
                <label htmlFor="quantity-input-ctrl">Qty:</label>
                <div className="counter-btn-shell">
                  <button onClick={() => setQuantity(q => Math.max(1, q - 1))} disabled={quantity <= 1 || isSubmitting}>-</button>
                  <span id="quantity-input-ctrl">{quantity}</span>
                  <button onClick={() => setQuantity(q => Math.min(product.stock, q + 1))} disabled={quantity >= product.stock || isSubmitting}>+</button>
                </div>
              </div>

              <button 
                className="add-to-cart-cta" 
                onClick={handleAddToCart}
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Adding...' : 'Add to Cart'}
              </button>
            </div>
          )}
        </section>
      </div>
    </main>
  );
};

export default ProductDetailPage;