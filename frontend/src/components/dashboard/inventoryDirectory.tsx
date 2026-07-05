import React, { useEffect, useState } from 'react';
import { productService } from '../../services/productService';
import { type ProductMinimalModel } from '../../types/product';
import './dashboardComponents.css';

interface InventoryDirectoryProps {
  onEditClick: (productId: number) => void;
  refreshTrigger: number;
  onMutationSuccess: () => void;
}

export const InventoryDirectory: React.FC<InventoryDirectoryProps> = ({ 
  onEditClick, 
  refreshTrigger,
  onMutationSuccess 
}) => {
  const [products, setProducts] = useState<ProductMinimalModel[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInventory = async () => {
    try {
      setIsLoading(true);
      const data = await productService.getSellerProductsAsync(page, 5);
      setProducts(data.items);
      setTotalPages(data.total_pages);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to sync inventory catalogs.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, [page, refreshTrigger]);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this listing?')) return;
    try {
      await productService.deleteProductAsync(id);
      onMutationSuccess();
      if (products.length === 1 && page > 1) {
        setPage(prev => prev - 1);
      } else {
        fetchInventory();
      }
    } catch (err: any) {
      alert(err.message || 'Could not complete deletion pipeline.');
    }
  };

  if (isLoading) return <div className="directory-loading-msg">Syncing listings data...</div>;
  if (error) return <div className="directory-error-msg">{error}</div>;

  return (
    <div className="inventory-management-section">
      <h3 className="section-inner-title">Live Storefront Inventory Directory</h3>
      
      <div className="table-responsive-wrapper">
        <table className="inventory-data-table">
          <thead>
            <tr>
              <th>Product Title</th>
              <th>Price Base</th>
              <th>Stock Level</th>
              <th style={{ textAlign: 'center' }}>Action Options</th>
            </tr>
          </thead>
          <tbody>
            {products.length === 0 ? (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', padding: '24px', color: 'var(--ash-grey)' }}>
                  No active listings detected. Add products to populate dashboards.
                </td>
              </tr>
            ) : (
              products.map((product) => (
                <tr key={product.id}>
                  <td className="product-name-cell">{product.name}</td>
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
                      <button 
                        type="button" 
                        className="action-inline-btn edit-btn"
                        onClick={() => onEditClick(product.id)}
                      >
                        ✏️ Edit
                      </button>
                      <button 
                        type="button" 
                        className="action-inline-btn delete-btn"
                        onClick={() => handleDelete(product.id)}
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="directory-pagination-bar">
          <button
            type="button"
            className="pagination-control-btn"
            disabled={page === 1}
            onClick={() => setPage(p => Math.max(p - 1, 1))}
          >
            Previous
          </button>
          <span className="pagination-index-indicator">
            Page {page} of {totalPages}
          </span>
          <button
            type="button"
            className="pagination-control-btn"
            disabled={page === totalPages}
            onClick={() => setPage(p => Math.min(p + 1, totalPages))}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};