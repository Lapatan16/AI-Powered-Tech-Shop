import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { type ProductMinimalModel } from '../../types/product';
import { productService } from '../../services/productService';
import { ProductGrid } from '../../components/productGrid/productGrid';
import './homePage.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [products, setProducts] = useState<ProductMinimalModel[]>([]);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const categoryId = searchParams.get('category_id') ? Number(searchParams.get('category_id')) : undefined;
  const subCategoryId = searchParams.get('sub_category_id') ? Number(searchParams.get('sub_category_id')) : undefined;
  const sortByPrice = (searchParams.get('sort_by_price') as 'asc' | 'desc' | '') || '';
  const currentPage = searchParams.get('page') ? Number(searchParams.get('page')) : 1;

  useEffect(() => {
    const fetchCatalogCollection = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data = await productService.getAllProductsAsync({
          category_id: categoryId,
          sub_category_id: subCategoryId,
          sort_by_price: sortByPrice,
          page: currentPage
        });

        setProducts(data.items);
        setTotalPages(data.total_pages);
      } catch (err: any) {
        setError(err.message || 'Something went wrong while fetching items.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCatalogCollection();
  }, [categoryId, subCategoryId, sortByPrice, currentPage]);

  const handleUpdateFilter = (key: string, value: string | number | undefined) => {
    const currentParams = new URLSearchParams(searchParams);
    currentParams.set('page', '1');

    if (value === undefined || value === '') {
      currentParams.delete(key);
    } else {
      currentParams.set(key, value.toString());
    }

    if (key === 'category_id') {
      currentParams.delete('sub_category_id');
    }

    setSearchParams(currentParams);
  };

  const handlePageChange = (targetPage: number) => {
    const currentParams = new URLSearchParams(searchParams);
    currentParams.set('page', targetPage.toString());
    setSearchParams(currentParams);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleClearAllFilters = () => {
    setSearchParams({});
  };

  return (
    <main className="home-page-main-div">
      <header className="home-page-header">
        <h1>Discover Products</h1>
        <p>Explore our latest professional collections</p>
      </header>

      <div className="catalog-toolbar-panel">
        <div className="filter-tags-indicator">
          {(categoryId || subCategoryId || sortByPrice) && (
            <button className="clear-all-btn" onClick={handleClearAllFilters}>
              Reset Filters ✕
            </button>
          )}
        </div>

        <div className="sort-dropdown-box">
          <label htmlFor="price-sort-select">Sort By: </label>
          <select
            id="price-sort-select"
            value={sortByPrice}
            onChange={(e) => handleUpdateFilter('sort_by_price', e.target.value)}
          >
            <option value="">Default Featured</option>
            <option value="asc">Price: Low to High</option>
            <option value="desc">Price: High to Low</option>
          </select>
        </div>
      </div>

      {isLoading && (
        <div className="home-page-status-message msg-loading">
          <div className="spinner"></div>
          <p>Updating database search mappings...</p>
        </div>
      )}

      {!isLoading && error && (
        <div className="home-page-status-message msg-error">
          <p>⚠️ Error: {error}</p>
        </div>
      )}

      {!isLoading && !error && products.length === 0 && (
        <div className="home-page-status-message msg-empty">
          <p>No products match your active filtering queries.</p>
          <button onClick={handleClearAllFilters}>View Full Catalog</button>
        </div>
      )}

      {!isLoading && !error && products.length > 0 && (
        <>
          <ProductGrid products={products} onProductClick={(id) => navigate(`/products/${id}`)} />
          
          {totalPages > 1 && (
            <div className="pagination-controls-rack">
              <button 
                disabled={currentPage === 1} 
                onClick={() => handlePageChange(currentPage - 1)}
              >
                &#10094; Previous
              </button>
              
              <span className="page-counter-label">
                Page <strong>{currentPage}</strong> of {totalPages}
              </span>

              <button 
                disabled={currentPage === totalPages} 
                onClick={() => handlePageChange(currentPage + 1)}
              >
                Next &#10095;
              </button>
            </div>
          )}
        </>
      )}
    </main>
  );
};

export default HomePage;