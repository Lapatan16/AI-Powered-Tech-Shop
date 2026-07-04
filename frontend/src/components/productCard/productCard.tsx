import React from 'react';
import { type ProductMinimalModel } from '../../types/product';
import './ProductCard.css';

interface ProductCardProps {
  product: ProductMinimalModel;
  onClick: (id: number) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onClick }) => {
  const hasDiscount = product.discount > 0;
  const finalPrice = hasDiscount 
    ? product.price * (1 - product.discount / 100) 
    : product.price;

  const displayImage = product.image || 'https://placehold.co/300x300?text=No+Image&font=roboto';

  return (
    <article className="product-card" onClick={() => onClick(product.id)}>
      <div className="product-card-image-wrapper">
        <img src={displayImage} alt={product.name} loading="lazy" />
        {hasDiscount && (
          <span className="product-card-badge">-{product.discount}%</span>
        )}
      </div>
      
      <div className="product-card-info">
        <h3 className="product-card-title">{product.name}</h3>
        
        <div className="product-card-price-container">
          {hasDiscount ? (
            <>
              <span className="price-old">${product.price.toFixed(2)}</span>
              <span className="price-current">${finalPrice.toFixed(2)}</span>
            </>
          ) : (
            <span className="price-current">${product.price.toFixed(2)}</span>
          )}
        </div>
      </div>
    </article>
  );
};