import React, { useState, useEffect } from 'react';
import { userService } from '../../services/userService';
import { type DashboardAnalyticsResponse, type MockProduct } from '../../types/user';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, BarChart, Bar
} from 'recharts';
import './DashboardPage.css';

const CHART_COLORS = ['#3182ce', '#319795', '#4c51bf', '#d69e2e', '#ecc94b'];

export const DashboardPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<DashboardAnalyticsResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [mockProducts, setMockProducts] = useState<MockProduct[]>([
    { id: 1, name: 'RGB Mechanical Gaming Keyboard', subcategory: 'Mechanical Boards', price: 149.99, stock: 2 },
    { id: 2, name: 'Logitech Superlight Pro', subcategory: 'Wireless Mice', price: 120.00, stock: 12 },
    { id: 3, name: 'USB-C Charging Hub 8-in-1', subcategory: 'Cables & Hubs', price: 45.50, stock: 0 }
  ]);

  useEffect(() => {
    const fetchDashboardAnalytics = async () => {
      try {
        const data = await userService.getDashboardAnalyticsAsync();
        setAnalytics(data);
      } catch (err: any) {
        setError(err.message || 'An unexpected error occurred loading analytics.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardAnalytics();
  }, []);

  const handleMockDelete = (id: number): void => {
    setMockProducts(prev => prev.filter(p => p.id !== id));
  };

  if (isLoading) return <div className="dashboard-loading">Loading configuration insights...</div>;
  if (error) return <div className="dashboard-error-alert">{error}</div>;

  return (
    <div className="dashboard-root-container">
      <div className="dashboard-header-row">
        <div>
          <h2 className="dashboard-title">✨ Seller Command Center</h2>
          <p className="dashboard-subtitle">Monitor storefront performance margins and operational stock logs.</p>
        </div>
      </div>

      <div className="metrics-summary-grid">
        <div className="metric-scorecard">
          <span className="card-icon">💰</span>
          <div className="card-info">
            <span className="card-label">Total Revenue</span>
            <h3 className="card-value">${analytics?.summary_metrics.total_revenue.toFixed(2)}</h3>
          </div>
        </div>

        <div className="metric-scorecard">
          <span className="card-icon">📦</span>
          <div className="card-info">
            <span className="card-label">Units Sold</span>
            <h3 className="card-value">{analytics?.summary_metrics.units_sold} Items</h3>
          </div>
        </div>

        <div className="metric-scorecard">
          <span className="card-icon">🏷️</span>
          <div className="card-info">
            <span className="card-label">Active Listings</span>
            <h3 className="card-value">{analytics?.summary_metrics.active_listings_count} Active</h3>
          </div>
        </div>

        <div className={`metric-scorecard ${analytics && analytics.summary_metrics.out_of_stock_count > 0 ? 'alert-border' : ''}`}>
          <span className="card-icon">⚠️</span>
          <div className="card-info">
            <span className="card-label">Out of Stock</span>
            <h3 className="card-value">{analytics?.summary_metrics.out_of_stock_count} Items</h3>
          </div>
        </div>
      </div>

      <div className="analytics-visualization-section">
        <h3 className="section-inner-title">Storefront Performance Margins</h3>
        <div className="charts-native-grid">
          
          <div className="chart-wrapper-card large-chart">
            <h4>📈 Daily Revenue Trend (Current Month)</h4>
            <div style={{ width: '100%', height: 200 }}>
              <ResponsiveContainer>
                <AreaChart data={analytics?.charts.revenue_trend} margin={{ top: 5, right: 15, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3182ce" stopOpacity={0.25}/>
                      <stop offset="95%" stopColor="#3182ce" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="date" stroke="#718096" fontSize={11} tickLine={false} />
                  <YAxis stroke="#718096" fontSize={11} tickLine={false} tickFormatter={(v) => `$${v}`} />
                  <Tooltip formatter={(value: any) => [`$${parseFloat(value).toFixed(2)}`, 'Revenue']} />
                  <Area type="monotone" dataKey="revenue" stroke="#3182ce" strokeWidth={1.5} fillOpacity={1} fill="url(#colorRevenue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-wrapper-card small-chart">
            <h4>🍩 Niche Value Distribution</h4>
            <div style={{ width: '100%', height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                  <Pie
                    data={analytics?.charts.category_distribution}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="40%"
                    innerRadius={45}
                    outerRadius={65}
                    paddingAngle={3}
                  >
                    {analytics?.charts.category_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: any) => [`$${parseFloat(value).toFixed(2)}`, 'Sales Total']} />
                  <Legend verticalAlign="bottom" height={24} iconType="circle" wrapperStyle={{ fontSize: '11px', bottom: 5 }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-wrapper-card full-width-chart">
            <h4>📊 Inventory Runway Velocity (Top Sellers)</h4>
            <div style={{ width: '100%', height: 200 }}>
              <ResponsiveContainer>
                <BarChart data={analytics?.charts.stock_vs_sales} margin={{ top: 10, right: 15, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#718096" fontSize={11} tickLine={false} />
                  <YAxis stroke="#718096" fontSize={11} tickLine={false} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: '11px' }} />
                  <Bar dataKey="sold" name="Units Sold" fill="#3182ce" barSize={18} radius={[3, 3, 0, 0]} />
                  <Bar dataKey="stock" name="Stock Remaining" fill="#cbd5e1" barSize={18} radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>

      <div className="inventory-management-section">
        <h3 className="section-inner-title">Live Storefront Inventory Directory</h3>
        <div className="table-responsive-wrapper">
          <table className="inventory-data-table">
            <thead>
              <tr>
                <th>Product Title</th>
                <th>Subcategory</th>
                <th>Price</th>
                <th>Stock Level</th>
                <th style={{ textAlign: 'center' }}>Action Options</th>
              </tr>
            </thead>
            <tbody>
              {mockProducts.map((product) => (
                <tr key={product.id}>
                  <td className="product-name-cell">{product.name}</td>
                  <td><span className="subcategory-badge">{product.subcategory}</span></td>
                  <td className="price-bold-text">${product.price.toFixed(2)}</td>
                  <td>
                    {product.stock === 0 ? (
                      <span className="stock-pill out-of-stock">Out of Stock</span>
                    ) : product.stock <= 5 ? (
                      <span className="stock-pill low-stock">Low Stock ({product.stock})</span>
                    ) : (
                      <span className="stock-pill healthy-stock">Healthy ({product.stock})</span>
                    )}
                  </td>
                  <td>
                    <div className="table-actions-flex">
                      <button type="button" className="action-inline-btn edit-btn" onClick={() => alert('Inline edit view')}>
                        ✏️ Edit
                      </button>
                      <button type="button" className="action-inline-btn delete-btn" onClick={() => handleMockDelete(product.id)}>
                        🗑️ Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};