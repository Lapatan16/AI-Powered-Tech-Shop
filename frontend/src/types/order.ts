export interface OrderItemResponse {
  product_name: string;
  price_at_purchase: number;
  quantity: number;
}

export interface OrderResponseModel {
  order_id: number;
  total_price: number;
  created_at: string;
  items: OrderItemResponse[];
}