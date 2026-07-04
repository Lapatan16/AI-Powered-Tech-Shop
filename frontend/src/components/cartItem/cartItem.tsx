import React from 'react';
import { type CartItemModel } from '../../types/cart';
import './cartItem.css';

interface CartItemProps {
  item: CartItemModel;
  onUpdateQuantity: (productId: number, currentAmount: number, change: number) => void;
  onRemove: (productId: number) => void;
}

export const CartItem: React.FC<CartItemProps> = ({ item, onUpdateQuantity, onRemove }) => {
  const fallbackImage = 'https://placehold.co/80x80?text=No+Image+Available&font=roboto';

  return (
    <div className="cart-item-row">
      <div className="cart-item-image-wrapper">
        <img src={item.image || fallbackImage} alt={item.name} />
      </div>

      <div className="cart-item-details">
        <h3 className="cart-item-title">{item.name}</h3>
        <p className="cart-item-unit-price">${item.price.toFixed(2)} each</p>
      </div>

      <div className="cart-item-quantity-management">
        <button 
          className="qty-adjust-btn" 
          onClick={() => onUpdateQuantity(item.product_id, item.amount, -1)}
          disabled={item.amount <= 1}
        >
          -
        </button>
        <span className="qty-value-indicator">{item.amount}</span>
        <button 
          className="qty-adjust-btn" 
          onClick={() => onUpdateQuantity(item.product_id, item.amount, 1)}
        >
          +
        </button>
      </div>

      <div className="cart-item-subtotal-block">
        <span className="item-calculated-subtotal">
          ${(item.price * item.amount).toFixed(2)}
        </span>
        <button className="cart-item-remove-btn" onClick={() => onRemove(item.product_id)}>
          Remove ✕
        </button>
      </div>
    </div>
  );
};