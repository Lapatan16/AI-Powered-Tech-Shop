export interface SummaryMetrics {
  total_revenue: number;
  units_sold: number;
  active_listings_count: number;
  out_of_stock_count: number;
}

export interface RevenueTrendPoint {
  date: string;
  revenue: number;
}

export interface CategoryDistributionPoint {
  name: string;
  value: number;
}

export interface StockVsSalesPoint {
  name: string;
  sold: number;
  stock: number;
}

export interface DashboardCharts {
  revenue_trend: RevenueTrendPoint[];
  category_distribution: CategoryDistributionPoint[];
  stock_vs_sales: StockVsSalesPoint[];
}

export interface DashboardAnalyticsResponse {
  summary_metrics: SummaryMetrics;
  charts: DashboardCharts;
}

export interface MockProduct {
  id: number;
  name: string;
  subcategory: string;
  price: number;
  stock: number;
}