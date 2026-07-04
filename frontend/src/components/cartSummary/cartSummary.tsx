import React from 'react';
import './cartSummary.css';

interface CartSummaryProps {
  subtotal: number;
  onCheckout: () => Promise<void>;
  isProcessing: boolean;
}

export const CartSummary: React.FC<CartSummaryProps> = ({ subtotal, onCheckout, isProcessing }) => {
  const estimatedShipping = subtotal > 150 ? 0 : 15.00;
  const estimatedTax = subtotal * 0.10;
  const checkoutGrandTotal = subtotal + estimatedShipping + estimatedTax;

  return (
    <div className="cart-summary-card">
      <h2>Order Summary</h2>
      <hr className="summary-divider" />
      
      <div className="summary-data-row">
        <span>Items Subtotal:</span>
        <strong>${subtotal.toFixed(2)}</strong>
      </div>
      
      <div className="summary-data-row">
        <span>Estimated Delivery:</span>
        <strong>{estimatedShipping === 0 ? 'FREE' : `$${estimatedShipping.toFixed(2)}`}</strong>
      </div>

      <div className="summary-data-row">
        <span>Sales Tax (10%):</span>
        <strong>${estimatedTax.toFixed(2)}</strong>
      </div>

      <hr className="summary-divider" />

      <div className="summary-data-row total-highlight">
        <span>Estimated Total:</span>
        <span>${checkoutGrandTotal.toFixed(2)}</span>
      </div>

      <button 
        className="checkout-cta-btn" 
        onClick={onCheckout}
        disabled={isProcessing || subtotal === 0}
      >
        {isProcessing ? 'Processing Order...' : 'Proceed to Checkout'}
      </button>
    </div>
  );
};