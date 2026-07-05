import React from 'react';
import { type ProductMinimalModel } from '../../types/product';
import { ProductCard } from '../productCard/productCard';
import './productGrid.css';

interface ProductGridProps {
  products: ProductMinimalModel[];
  onProductClick: (id: number) => void;
}

export const ProductGrid: React.FC<ProductGridProps> = ({ products, onProductClick }) => {
  return (
    <div className="product-grid">
      {products.map((product) => (
        <ProductCard 
          key={product.id} 
          product={product} 
          onClick={onProductClick} 
        />
      ))}
    </div>
  );
};