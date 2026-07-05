import React, { useState, useEffect } from 'react';
import { userService } from '../../services/userService';
import { type DashboardAnalyticsResponse } from '../../types/user';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, BarChart, Bar
} from 'recharts';
import { InventoryDirectory } from '../../components/dashboard/inventoryDirectory';
import { EditProductModal } from '../../components/dashboard/editProductModal';
import './dashboardPage.css';

const PALETTE_COLORS = ['#3b413c', '#94d1be', '#9db5b2', '#daf0ee', '#744210'];

export const DashboardPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<DashboardAnalyticsResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const [activeEditingId, setActiveEditingId] = useState<number | null>(null);

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

  useEffect(() => {
    fetchDashboardAnalytics();
  }, [refreshKey]);

  const handleDataMutation = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleNavigateToCreate = () => {
    window.location.href = '/create-product';
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
        <button className="create-product-trigger-btn" onClick={handleNavigateToCreate}>
          <span className="plus-symbol-icon">＋</span> Add New Product
        </button>
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
                      <stop offset="5%" stopColor="#94d1be" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#94d1be" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#daf0ee" />
                  <XAxis dataKey="date" stroke="#9db5b2" fontSize={11} tickLine={false} />
                  <YAxis stroke="#9db5b2" fontSize={11} tickLine={false} tickFormatter={(v) => `$${v}`} />
                  <Tooltip contentStyle={{ background: '#ffffffff', borderColor: '#daf0eeff' }} formatter={(value: any) => [`$${parseFloat(value).toFixed(2)}`, 'Revenue']} />
                  <Area type="monotone" dataKey="revenue" stroke="#3b413c" strokeWidth={2} fillOpacity={1} fill="url(#colorRevenue)" />
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
                    {analytics?.charts.category_distribution.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={PALETTE_COLORS[index % PALETTE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: any) => [`$${parseFloat(value).toFixed(2)}`, 'Sales Total']} />
                  <Legend verticalAlign="bottom" height={24} iconType="circle" wrapperStyle={{ fontSize: '11px', bottom: 5, color: '#3b413c' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-wrapper-card full-width-chart">
            <h4>📊 Inventory Runway Velocity (Top Sellers)</h4>
            <div style={{ width: '100%', height: 200 }}>
              <ResponsiveContainer>
                <BarChart data={analytics?.charts.stock_vs_sales} margin={{ top: 10, right: 15, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#daf0ee" />
                  <XAxis dataKey="name" stroke="#9db5b2" fontSize={11} tickLine={false} />
                  <YAxis stroke="#9db5b2" fontSize={11} tickLine={false} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: '11px' }} />
                  <Bar dataKey="sold" name="Units Sold" fill="#3b413c" barSize={18} radius={[3, 3, 0, 0]} />
                  <Bar dataKey="stock" name="Stock Remaining" fill="#9db5b2" barSize={18} radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>

      <InventoryDirectory 
        onEditClick={(id) => setActiveEditingId(id)}
        refreshTrigger={refreshKey}
        onMutationSuccess={handleDataMutation}
      />

      {activeEditingId !== null && (
        <EditProductModal 
          productId={activeEditingId}
          onClose={() => setActiveEditingId(null)}
          onUpdateSuccess={handleDataMutation}
        />
      )}
    </div>
  );
};