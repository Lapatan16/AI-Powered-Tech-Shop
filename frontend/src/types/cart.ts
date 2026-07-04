export interface CartItemModel {
  product_in_cart_id: number;
  product_id: number;
  name: string;
  amount: number;
  price: number;
  image: string | null;
}

export interface CartModel {
  cart_id: number;
  user_id: number;
  items: CartItemModel[];
}

export interface CartUpdatePayload {
  product_id: number;
  new_amount: number;
  increase: boolean;
}