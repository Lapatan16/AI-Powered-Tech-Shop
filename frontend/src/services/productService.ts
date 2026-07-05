import type { CategoryTreeModel } from '../types/category';
import {
  type AiProductPredictionModel,
  type PaginatedProductsModel,
  type ProductCreateModel,
  type ProductDetailModel,
  type ProductMinimalModel,
  type ProductUpdateModel
} from '../types/product';
import { apiClient } from './apiClient';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const productService = {
  async getAllProductsAsync(filters: {
    category_id?: number;
    sub_category_id?: number;
    sort_by_price?: 'asc' | 'desc' | '';
    page?: number;
  } = {}): Promise<PaginatedProductsModel> {
    
    const queryParams = new URLSearchParams();
    if (filters.category_id) queryParams.append('category_id', filters.category_id.toString());
    if (filters.sub_category_id) queryParams.append('sub_category_id', filters.sub_category_id.toString());
    if (filters.sort_by_price) queryParams.append('sort_by_price', filters.sort_by_price);
    if (filters.page) queryParams.append('page', filters.page.toString());

    const response = await fetch(`${API_BASE_URL}/products/all?${queryParams.toString()}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }

    return response.json();
  },

  async getProductByIdAsync(productId: number): Promise<ProductDetailModel> {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      if (response.status === 404) throw new Error('Product not found.');
      throw new Error('Server encountered an issue loading product information.');
    }

    return response.json();
  },

  async getAIRecommendationsAsync(): Promise<ProductMinimalModel[]> {
    return apiClient.requestAsync<ProductMinimalModel[]>('/recommendations/for-you', {
      method: 'GET'
    });
  },

  async createProductAsync(productData: ProductCreateModel): Promise<ProductMinimalModel> {
    const formData = new FormData();
    
    formData.append('name', productData.name);
    formData.append('description', productData.description);
    formData.append('sub_category_id', productData.sub_category_id.toString());
    formData.append('price', productData.price.toString());
    formData.append('stock', productData.stock.toString());
    formData.append('discount', productData.discount.toString());

    productData.images.forEach((file) => {
      formData.append('images', file);
    });

    return apiClient.requestAsync<ProductMinimalModel>('/products/', {
      method: 'POST',
      body: formData
    });
  },

  async autocompleteProductFieldsAsync(userPrompt: string): Promise<AiProductPredictionModel> {
    return apiClient.requestAsync<AiProductPredictionModel>('/recommendations/autofill', {
      method: 'POST',
      body: JSON.stringify({ user_prompt: userPrompt }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
  },

  async getSellerProductsAsync(page: number = 1, limit: number = 10): Promise<PaginatedProductsModel> {
    return apiClient.requestAsync<PaginatedProductsModel>(`/products/seller/mine?page=${page}&limit=${limit}`, {
      method: 'GET'
    });
  },

  async updateProductAsync(productId: number, data: ProductUpdateModel): Promise<ProductMinimalModel> {
    return apiClient.requestAsync<ProductMinimalModel>(`/products/${productId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    });
  },

  async deleteProductAsync(productId: number): Promise<void> {
    return apiClient.requestAsync<void>(`/products/${productId}`, {
      method: 'DELETE'
    });
  },

  async getAllCategoriesAsync(): Promise<CategoryTreeModel[]> {
    const response = await fetch('http://localhost:9061/products/categories/all');
    if (!response.ok) {
      throw new Error('Failed to fetch category selections.');
    }
    return response.json();
  }
}