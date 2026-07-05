export interface ImageEntity {
  id: number;
  src: string;
}

export interface ProductEntity {
  id: number;
  name: string;
  description: string;
  sub_category_id: number;
  user_id: number;
  price: number;
  stock: number;
  discount: number;
  images: ImageEntity[];
}

export interface ProductMinimalModel {
  id: number;
  name: string;
  price: number;
  stock: number;
  sub_category_id: number;
  discount: number;
  image: string | null;
}

export interface ProductDetailModel {
  id: number;
  name: string;
  description: string;
  sub_category_id: number;
  user_id: number;
  price: number;
  stock: number;
  discount: number;
  images: string[];
}

export interface PaginatedProductsModel {
  items: ProductMinimalModel[];
  total_records: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface ProductCreateModel {
  name: string;
  description: string;
  sub_category_id: number;
  price: number;
  stock: number;
  discount: number;
  images: File[];
}

export interface AiProductPredictionModel {
  name: string;
  description: string;
  sub_category_id: number;
  parent_category_id: number;
  price: number;
  stock: number;
  discount: number;
}

export interface ProductUpdateModel {
  name: string;
  description: string;
  sub_category_id: number;
  price: number;
  stock: number;
  discount: number;
}

export interface BackendCategoryMinimal {
  id: number;
  name: string;
}

export interface BackendSubCategoryMinimal {
  id: number;
  name: string;
  category: BackendCategoryMinimal;
}

export interface BackendSellerMinimal {
  id: number;
  user_name: string;
  email: string;
}

export interface BackendProductDetail {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  discount: number;
  images: string[];
  seller: BackendSellerMinimal;
  sub_category: BackendSubCategoryMinimal;
}