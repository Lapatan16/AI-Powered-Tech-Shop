import React, { useState, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { createPortal } from 'react-dom';
import { productService } from '../../services/productService';
import { type ProductCreateModel } from '../../types/product';
import { type CategoryTreeModel } from '../../types/category';
import './CreateProductPage.css';

export const CreateProductPage: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [price, setPrice] = useState<string>('0.0');
  const [stock, setStock] = useState<string>('1');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  
  const [categories, setCategories] = useState<CategoryTreeModel[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>('');
  const [subCategoryId, setSubCategoryId] = useState<string>('');

  const matchedCategory = categories.find(c => c.id.toString() === selectedCategoryId);
  const availableSubCategories = matchedCategory ? matchedCategory.sub_categories : [];

  const [isAiModalOpen, setIsAiModalOpen] = useState<boolean>(false);
  const [aiPrompt, setAiPrompt] = useState<string>('');
  const [isAiProcessing, setIsAiProcessing] = useState<boolean>(false);

  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchNavigationTree = async () => {
      try {
        const response = await fetch('http://localhost:9061/products/categories/all');
        if (response.ok) {
          const data = await response.json();
          setCategories(data);
        } else {
          setErrorMessage('Failed to fetch product selection categories.');
        }
      } catch (error) {
        console.error('Failed to load menu layers:', error);
        setErrorMessage('Could not load categories from backend.');
      }
    };
    fetchNavigationTree();
  }, []);

  const handleCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategoryId(e.target.value);
    setSubCategoryId(''); 
  };

  const handleAiAutocompleteSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsAiProcessing(true);
    setErrorMessage(null);

    try {
      const predictedData = await productService.autocompleteProductFieldsAsync(aiPrompt);
      
      setName(predictedData.name);
      setDescription(predictedData.description);
      setPrice(predictedData.price.toString());
      setStock(predictedData.stock.toString());
      
      setSelectedCategoryId(predictedData.parent_category_id.toString());
      setSubCategoryId(predictedData.sub_category_id.toString());

      setIsAiModalOpen(false);
      setAiPrompt('');
    } catch (err: any) {
      setErrorMessage(err.message || 'The AI service was unable to parse your description. Please fill manually.');
    } finally {
      setIsAiProcessing(false);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      setSelectedFiles((prevFiles) => [...prevFiles, ...filesArray]);
    }
  };

  const removeFile = (indexToRemove: number) => {
    setSelectedFiles((prevFiles) => prevFiles.filter((_, idx) => idx !== indexToRemove));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setSuccessMessage(null);

    if (!subCategoryId) {
      setErrorMessage('Please select a subcategory for your item.');
      return;
    }

    if (selectedFiles.length === 0) {
      setErrorMessage('You must upload at least one image of your product.');
      return;
    }

    setIsSubmitting(true);

    const payload: ProductCreateModel = {
      name,
      description,
      sub_category_id: Number(subCategoryId),
      price: parseFloat(price),
      stock: parseInt(stock, 10),
      discount: 0.0, 
      images: selectedFiles,
    };

    try {
      const createdProduct = await productService.createProductAsync(payload);
      setSuccessMessage(`Success! "${createdProduct.name}" has been placed for sale.`);
      
      setName('');
      setDescription('');
      setSelectedCategoryId('');
      setSubCategoryId('');
      setPrice('0.0');
      setStock('1');
      setSelectedFiles([]);
    } catch (err: any) {
      setErrorMessage(err?.message || 'Something went wrong while posting your item.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="create-product-container">
      <div className="form-card-wrapper">
        <div className="form-header-row">
          <div>
            <h2 className="form-title">List an Item for Sale</h2>
            <p className="form-subtitle">Fill in the fields below to create your product listing.</p>
          </div>
          <button 
            type="button" 
            className="ai-action-trigger-btn"
            onClick={() => setIsAiModalOpen(true)}
          >
            ✨ AI Auto-Fill
          </button>
        </div>

        {errorMessage && <div className="alert-box error-alert">{errorMessage}</div>}
        {successMessage && <div className="alert-box success-alert">{successMessage}</div>}

        <form onSubmit={handleSubmit} className="product-sale-form">
          <div className="input-group">
            <label htmlFor="prod-name">Product Name *</label>
            <input
              id="prod-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Mechanical RGB Gaming Keyboard"
              required
            />
          </div>

          <div className="form-row-grid">
            <div className="input-group">
              <label htmlFor="prod-cat">Category *</label>
              <select
                id="prod-cat"
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

            <div className="input-group">
              <label htmlFor="prod-subcat">Subcategory *</label>
              <select
                id="prod-subcat"
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

          <div className="form-row-grid">
            <div className="input-group">
              <label htmlFor="prod-price">Price ($) *</label>
              <input
                id="prod-price"
                type="number"
                step="0.01"
                min="0"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="prod-stock">Available Stock *</label>
              <input
                id="prod-stock"
                type="number"
                min="1"
                value={stock}
                onChange={(e) => setStock(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="prod-desc">Item Description</label>
            <textarea
              id="prod-desc"
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Provide a detailed overview of your product..."
            />
          </div>

          <div className="input-group images-upload-section">
            <label>Product Images * <span className="label-hint">(At least 1 required)</span></label>
            
            <div className="file-drop-zone">
              <input
                id="file-input-element"
                type="file"
                multiple
                accept="image/*"
                onChange={handleFileChange}
                className="hidden-file-input"
              />
              <label htmlFor="file-input-element" className="file-upload-trigger-btn">
                <span>📷</span> Choose Product Images
              </label>
            </div>

            {selectedFiles.length > 0 && (
              <div className="file-previews-list">
                {selectedFiles.map((file, idx) => (
                  <div key={`${file.name}-${idx}`} className="file-preview-chip">
                    <span className="file-name-text">{file.name}</span>
                    <button type="button" onClick={() => removeFile(idx)} className="remove-file-btn">
                      &times;
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button type="submit" disabled={isSubmitting} className="submit-form-action-btn">
            {isSubmitting ? 'Posting Item...' : 'List Product Now'}
          </button>
        </form>
      </div>

      {isAiModalOpen && createPortal(
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(59, 65, 60, 0.6)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 999999,
            backdropFilter: 'blur(4px)',
            boxSizing: 'border-box'
          }}
        >
          <div 
            style={{
              backgroundColor: '#ffffff',
              padding: '28px',
              borderRadius: '12px',
              width: '90%',
              maxWidth: '500px',
              boxShadow: '0 10px 30px rgba(0, 0, 0, 0.15)',
              boxSizing: 'border-box'
            }}
          >
            <h3 className="modal-title">✨ Describe Your Product</h3>
            <p className="modal-subtitle">Tell the AI what you are selling, its configuration details, or its target value, and let it draft your listing requirements.</p>
            
            <form onSubmit={handleAiAutocompleteSubmit}>
              <textarea
                className="modal-prompt-textarea"
                rows={5}
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                placeholder="e.g. Selling a logitech superlight wireless mouse mouse white color used for a month, price 150 dollars..."
                required
              />
              
              <div className="modal-actions-container">
                <button 
                  type="button" 
                  className="modal-cancel-btn"
                  onClick={() => { setIsAiModalOpen(false); setAiPrompt(''); }}
                  disabled={isAiProcessing}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="modal-generate-btn"
                  disabled={isAiProcessing}
                >
                  {isAiProcessing ? 'Analyzing...' : 'Generate Form Data'}
                </button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};