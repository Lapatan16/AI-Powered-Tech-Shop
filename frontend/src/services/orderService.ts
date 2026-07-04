import type { OrderResponseModel } from '../types/order';
import { apiClient } from './apiClient';

export const orderService = {
  async checkoutCartAsync(): Promise<OrderResponseModel> {
    return await apiClient.requestAsync<OrderResponseModel>('/orders/checkout', {
      method: 'POST',
    });
  },
};