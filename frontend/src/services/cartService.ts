import { apiClient } from './apiClient';
import { type CartModel, type CartUpdatePayload } from '../types/cart';

export const cartService = {
  async getCartForUserAsync(): Promise<CartModel> {
    return apiClient.requestAsync<CartModel>('/carts/items', {
      method: 'GET',
    });
  },

  async addProductToCartAsync(productId: number, amount: number): Promise<void> {
    return apiClient.requestAsync<void>('/carts/add-product', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, amount }),
    });
  },

  async removeProductFromCartAsync(productId: number): Promise<void> {
    return apiClient.requestAsync<void>(`/carts/remove-product/${productId}`, {
      method: 'DELETE',
    });
  },

  async updateQuantityAsync(payload: CartUpdatePayload): Promise<any> {
    return apiClient.requestAsync<any>('/carts/update-product-quantity', {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  }
};