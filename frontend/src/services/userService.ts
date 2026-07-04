import { apiClient } from './apiClient';
import { type DashboardAnalyticsResponse } from '../types/user';

export const userService = {
  async getDashboardAnalyticsAsync(): Promise<DashboardAnalyticsResponse> {
    return apiClient.requestAsync<DashboardAnalyticsResponse>('/users/dashboard/analytics', {
      method: 'GET',
    });
  }
};