import React, { useState, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { productService } from '../../services/productService';
import { type BackendProductDetail, type ProductUpdateModel } from '../../types/product';
import { type CategoryTreeModel } from '../../types/category';

interface EditProductModalProps {
  productId: number;
  onClose: () => void;
  onUpdateSuccess: () => void;
}

export const EditProductModal: React.FC<EditProductModalProps> = ({ productId, onClose, onUpdateSuccess }) => {
  const [name, setName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [price, setPrice] = useState<string>('0.0');
  const [stock, setStock] = useState<string>('0');
  const [discount, setDiscount] = useState<number>(0);

  const [categories, setCategories] = useState<CategoryTreeModel[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>('');
  const [subCategoryId, setSubCategoryId] = useState<string>('');

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const matchedCategory = categories.find(c => c.id.toString() === selectedCategoryId);
  const availableSubCategories = matchedCategory ? matchedCategory.sub_categories : [];

  useEffect(() => {
    let isMounted = true;

    const initializeModalData = async () => {
      try {
        setIsLoading(true);
        
        const categoriesData = await productService.getAllCategoriesAsync();
        const product = await productService.getProductByIdAsync(productId) as unknown as BackendProductDetail;
        
        if (!isMounted) return;

        setCategories(categoriesData);
        setName(product.name || '');
        setDescription(product.description || '');
        setPrice(product.price !== undefined ? product.price.toString() : '0.0');
        setStock(product.stock !== undefined ? product.stock.toString() : '0');
        setDiscount(product.discount || 0);

        if (product.sub_category) {
          setSelectedCategoryId(product.sub_category.category.id.toString());
          setSubCategoryId(product.sub_category.id.toString());
        }

      } catch (err: any) {
        alert(err.message || 'Failed to extract product detail records.');
        onClose();
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    initializeModalData();

    return () => {
      isMounted = false;
    };
  }, [productId]);

  const handleCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategoryId(e.target.value);
    setSubCategoryId('');
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!subCategoryId) {
      alert('Please select a subcategory for your item.');
      return;
    }

    try {
      setIsSubmitting(true);
      const payload: ProductUpdateModel = {
        name,
        description,
        sub_category_id: Number(subCategoryId),
        price: parseFloat(price),
        stock: parseInt(stock, 10),
        discount
      };
      await productService.updateProductAsync(productId, payload);
      onUpdateSuccess();
      onClose();
    } catch (err: any) {
      alert(err.message || 'Verification update cycle failed.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop-overlay">
      <div className="modal-content-card">
        <h3 className="modal-inner-heading">✏️ Modify Product Configuration</h3>
        
        {isLoading ? (
          <div style={{ padding: '40px 0', textAlign: 'center', color: '#9db5b2' }}>
            Retrieving product records...
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="modal-transactional-form">
            
            <div className="modal-input-group">
              <label htmlFor="edit-prod-name">PRODUCT TITLE *</label>
              <input 
                id="edit-prod-name"
                type="text" 
                required 
                value={name}
                onChange={e => setName(e.target.value)}
              />
            </div>

            <div className="modal-form-row-grid">
              <div className="modal-input-group">
                <label htmlFor="edit-prod-cat">CATEGORY *</label>
                <select
                  id="edit-prod-cat"
                  value={selectedCategoryId}
                  onChange={handleCategoryChange}
                  required
                >
                  <option value="">-- Choose Category --</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="modal-input-group">
                <label htmlFor="edit-prod-subcat">SUBCATEGORY *</label>
                <select
                  id="edit-prod-subcat"
                  value={subCategoryId}
                  onChange={(e) => setSubCategoryId(e.target.value)}
                  disabled={!selectedCategoryId}
                  required
                >
                  <option value="">-- Choose Subcategory --</option>
                  {availableSubCategories.map((subcat) => (
                    <option key={subcat.id} value={subcat.id}>
                      {subcat.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="modal-form-row-grid">
              <div className="modal-input-group">
                <label htmlFor="edit-prod-price">PRICE ($) *</label>
                <input 
                  id="edit-prod-price"
                  type="number" 
                  step="0.01" 
                  required 
                  value={price}
                  onChange={e => setPrice(e.target.value)}
                />
              </div>
              <div className="modal-input-group">
                <label htmlFor="edit-prod-stock">STOCK UNITS *</label>
                <input 
                  id="edit-prod-stock"
                  type="number" 
                  required 
                  value={stock}
                  onChange={e => setStock(e.target.value)}
                />
              </div>
            </div>

            <div className="modal-input-group">
              <label htmlFor="edit-prod-desc">DESCRIPTION *</label>
              <textarea 
                id="edit-prod-desc"
                rows={3} 
                required 
                value={description}
                onChange={e => setDescription(e.target.value)}
              />
            </div>

            <div className="modal-actions-wrapper">
              <button 
                type="button" 
                className="modal-secondary-btn" 
                onClick={onClose} 
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="modal-primary-btn" 
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Saving changes...' : 'Save Configuration'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};