import React, { useEffect, useState } from 'react';
import { cartService } from '../../services/cartService';
import { orderService } from '../../services/orderService';
import { type CartModel } from '../../types/cart';
import { CartItem } from '../../components/cartItem/cartItem';
import { CartSummary } from '../../components/cartSummary/cartSummary';
import './cartPage.css';

export const CartPage: React.FC = () => {
  const [cart, setCart] = useState<CartModel | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchActiveCart = async () => {
    try {
      setIsLoading(true);
      const data = await cartService.getCartForUserAsync();
      setCart(data);
    } catch (err: any) {
      setError(err.message || 'Could not retrieve your digital shopping items profile.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchActiveCart();
  }, []);

  const handleCheckout = async () => {
    try {
      setIsSubmitting(true);
      const receipt = await orderService.checkoutCartAsync();
      
      setCart({ ...cart!, items: [] });
      
      alert(`Success! Order #${receipt.order_id} processed for a total of $${receipt.total_price.toFixed(2)}.`);
      
      window.location.href = '/';
    } catch (err: any) {
      alert(err.message || 'Checkout failed. Please check store product availability limits.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateItemQuantity = async (productId: number, currentAmount: number, change: number) => {
    if (!cart) return;
    try {
      const isIncrease = change > 0;
      const targetAmount = isIncrease ? currentAmount + 1 : currentAmount - 1;

      setCart({
        ...cart,
        items: cart.items.map(item => 
          item.product_id === productId ? { ...item, amount: targetAmount } : item
        )
      });

      await cartService.updateQuantityAsync({
        product_id: productId,
        new_amount: targetAmount,
        increase: isIncrease
      });
    } catch (err: any) {
      fetchActiveCart();
      alert('Failed to accurately update item counts: ' + err.message);
    }
  };

  const handleRemoveProduct = async (productId: number) => {
    if (!cart) return;
    try {
      setCart({
        ...cart,
        items: cart.items.filter(item => item.product_id !== productId)
      });
      await cartService.removeProductFromCartAsync(productId);
    } catch (err: any) {
      fetchActiveCart();
      alert('Failed to remove targeted entity from current tracking state.');
    }
  };

  if (isLoading) {
    return (
      <div className="cart-loading-box">
        <div className="spinner"></div>
        <p>Syncing items with active store stock...</p>
      </div>
    );
  }

  if (error) {
    return <div className="cart-error-banner">⚠️ Failed to synchronize checkout values: {error}</div>;
  }

  const itemsCount = cart?.items.reduce((acc, item) => acc + item.amount, 0) || 0;
  const itemsSubtotalValue = cart?.items.reduce((acc, item) => acc + (item.price * item.amount), 0) || 0;

  return (
    <main className="cart-page-outer-container">
      {isSubmitting && <div className="checkout-processing-overlay"><div className="spinner"></div>Processing Order...</div>}

      <header className="cart-page-header">
        <h1>Your Shopping Cart</h1>
        <p>You have <strong>{itemsCount}</strong> item(s) staged in your layout workspace.</p>
      </header>

      {!cart || cart.items.length === 0 ? (
        <div className="empty-cart-fallback-card">
          <p>Your shopping cart is currently empty.</p>
          <button className="return-shop-btn" onClick={() => window.location.href = '/'}>
            Discover Products
          </button>
        </div>
      ) : (
        <div className="cart-split-grid-layout">
          <section className="cart-items-collection-pane">
            {cart.items.map(item => (
              <CartItem 
                key={item.product_in_cart_id} 
                item={item} 
                onUpdateQuantity={handleUpdateItemQuantity}
                onRemove={handleRemoveProduct}
              />
            ))}
          </section>

          <section className="cart-summary-aggregation-pane">
            <CartSummary 
              subtotal={itemsSubtotalValue} 
              onCheckout={handleCheckout} 
              isProcessing={isSubmitting}
            />
          </section>
        </div>
      )}
    </main>
  );
};

export default CartPage;